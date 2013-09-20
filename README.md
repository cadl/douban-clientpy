# douban-clientpy

豆瓣v2 api python版sdk

## 用法

### 初始化

`import douban`

创建`client`对象

`c = douban.APIClient('Your API Key', 'Secret', 'redirect_url', 'code', ['douban_basic_common','book_basic_r'])`

通过 `authorize_url` 授权获得`access_token`

`url = c.authorize_url`

`c.gen_access_token('授权后redirect_url中的参数code')`

或

设置已保存的`access_token`

`c.set_access_token({'access_token': xxx, 'expires_in': xxx, 'refresh_token': xxx, 'douban_user_id': xxx})`

或

刷新 `access_token`

`c.refresh_access_token()`

### 调用api

例子

>获取图书信息    GET /v2/book/:id

`c.get__v2__book__id('bookid')`

>用户收藏某本图书   POST    /v2/book/:id/collection

`c.post__v2__book__id__collection('bookidd', status='xxx', tags='xxx')`
