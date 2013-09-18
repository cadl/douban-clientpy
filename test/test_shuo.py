import base
import uuid


class TestApiShuo(base.ApiClientTestBase):
    def setUp(self):
        super(TestApiShuo, self).setUp()
        self.text = 'test' + uuid.uuid4().hex
        self.status_id = '1222661567'
        self.img = open('1.png')
        self.rec_title = 'sgap'
        self.rec_url = 'http://www.douban.com/people/78123615/'
        self.rec_desc = 'sb|!sb'
        self.rec_image = 'http://img3.douban.com/view/photo/photo/public/p2040572454.jpg'

    def test_statuses_not_with_img(self):
        ret = self.client.post__shuo__v2__statuses__(text=self.text,
                rec_title=self.rec_title, rec_url=self.rec_url,
                rec_desc=self.rec_desc, rec_image=self.rec_image)
        self.assertIsInstance(ret, dict)

    def test_statuses_with_img(self):
        ret = self.client.post__shuo__v2__statuses__(text=self.text,
                image=self.img)
        self.assertIsInstance(ret, dict)
    
    def test_statuses_home_timeline(self):
        ret = self.client.get__shuo__v2__statuses__home_timeline()
        self.assertIsInstance(ret, list)

    def tearDown(self):
        self.img.close()
