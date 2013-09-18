import unittest
import douban
from appconf import API_KEY, SECRET, CALLBACK_URL, RESPONSE_TYPE


class ApiClientTestBase(unittest.TestCase):
    def setUp(self):
        self.client = client
         

def get_client():
    client = douban.APIClient(API_KEY, SECRET,
              CALLBACK_URL, RESPONSE_TYPE)
    print 'get code from callback url'
    print client.authorize_url
    code = raw_input()
    client.gen_access_token(code)
    return client

client = get_client()
