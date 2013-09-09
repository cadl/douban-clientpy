import requests
import urllib


API_URL = 'https://api.douban.com/'
AUTH_URL = 'https://www.douban.com/service/auth2/auth'
TOKEN_URL = 'https://www.douban.com/service/auth2/token'


class APIError(StandardError):
    '''api error'''
    def __init__(self, error_code, msg, request):
        self.error_code = error_code
        self.msg = msg
        self.request = request
        StandardError.__init__(self, msg)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code,
                self.msg, self.request)


class APIClient(object):
    def __init__(self, api_key, secret, redirect_url,
            response_type, scope=None, state=None):
        self.__client_id = api_key
        self.__secret = secret
        self.__redirect_url = redirect_url
        self.__response_type = response_type
        self.__scope = scope
        self.__state = state
        self.__access_token = None
        self.__expires_in = None
        self.__refresh_token = None
        self.__douban_user_id = None
        self.__headers = {}

    def __getattr__(self, attr):
        l = attr.split('__')
        method = l.pop(0)
        if not method in ('get', 'post', 'put', 'delete'):
            raise AttributeError
        def wrapper(*args, **kwargs):
            for index, val in enumerate(l):
                if val in ['id', 'name']:
                    l[index] = '%s'
            path = API_URL + '/'.join(l) + '/'
            kwargs['source'] = self.__client_id
            if args:
                path = path % args
            if method == 'post':
                files = {}
                if 'image' in kwargs:
                    files['image'] = kwargs.pop('image')
                req = requests.request(method.upper(), path,
                        headers=self.__headers, files=files, data=kwargs)
            elif method == 'get':
                req = requests.request(method.upper(), path,
                        headers=self.__headers, params=kwargs)
            else:
                req = requests.request(method.upper(), path,
                        headers=self.__headers)
            self._check_exception(req)
            return req.json()
        return wrapper
        
    @property
    def authorize_url(self):
        param_dict = {
                'client_id': self.__client_id,
                'redirect_uri': self.__redirect_url,
                'response_type': self.__response_type
                }
        if self.__scope:
            param_dict['scope'] = ','.join(self.__scope)
        if self.__state:
            param_dict['state'] = self.__state
        param = urllib.urlencode(param_dict)
        return "%s?%s" % (AUTH_URL, param)

    def gen_access_token(self, code):
        param_dict = {
                'client_id': self.__client_id,
                'client_secret': self.__secret,
                'redirect_uri': self.__redirect_url,
                'grant_type': 'authorization_code',
                'code': code
                }
        r = requests.post(TOKEN_URL, data=param_dict)
        ret = r.json()
        if not r.status_code == 200:
            raise APIError(ret['code'], ret['msg'], ret['request'])

        self.__access_token = ret['access_token'] 
        self.__expires_in = ret['expires_in']
        self.__refresh_token = ret['refresh_token']
        self.__douban_user_id = ret['douban_user_id']
        self.__headers['Authorization'] = 'Bearer %s' % (self.__access_token)
        return ret

    def set_access_token(self, d):
        '''d is a dict include {'access_token': XXX, 'expires_in': XXX, 'refresh_token': XXX, 'douban_user_id': XXX}'''
        self.__access_token = d['access_token']
        self.__expires_in = d['expires_in']
        self.__refresh_token = d['refresh_token']
        self.__douban_user_id = d['douban_user_id']
        self.__headers['Authorization'] = 'Bearer %s' % (self.__access_token)

    def refresh_access_token(self):
        param_dict = {
                'client_id': self.__client_id,
                'client_secret': self.__secret,
                'redirect_uri': self.__redirect_url,
                'grant_type': 'refresh_token',
                'code': self.refresh_token or ''
                }
        r = requests.post(TOKEN_URL, data=param_dict)
        ret = r.json()
        if not r.status_code == 200:
            raise APIError(ret['code'], ret['msg'], ret['request'])
        self.__access_token = ret['access_token']
        self.__expires_in = ret['expires_in']
        self.__refresh_token = ret['refresh_token']
        self.__douban_user_id = ret['douban_user_id']
        self.__headers['Authorization'] = 'Bearer %s' % (self.__access_token)
        return ret

    def _check_exception(self, obj):
        if obj.status_code >= 400:
            ret = obj.json()
            self.__path = API_URL
            raise APIError(ret.get('code', 'unkown'), ret.get('msg', 'unkown'), ret.get('request', 'unkown'))
