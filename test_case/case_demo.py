import unittest

import requests
from ddt import file_data
from wx.lib.pubsub.core import kwargs

from api_key.keys import Key
from conf import readconf
from demo.demo import res


class Case(unittest.TestCase):
    # unittest 下面遵循unittest方法去做
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = Key()
        # 创建一个类的初始化setup对象叫key对象
        cls.token = None
        cls.userid = None
        cls.openid = None
        cls.cardid = None
        # cls.url = 'http://127.0.0.1:5000'
        cls.url = readconf.read('../conf/conf.ini', 'TEST', 'url')

        # 自动化赋值
        '''
        将数据文件中需要赋值的key,进行全局变量赋值，要求这些key与全局变量要一一对应
        1、先将文件传过来 kwags ,for 循环将key ,v 读取出来
        '''
    def assignment(self, kwargs):
        for k, v in kwargs.item():
            # 如果是字典继续解析，直到不是字典为止
            if type(v) is dict:
                self.assignment(v)
            else:
                # v有值
                if v:
                    pass
                else:  # v没有值，进行反射赋值
                    kwargs[k] = getattr(self, k)
            return kwargs

    def test_01_login(self):
        # key = Key()

        login_url = 'http://127.0.0.1:5000/api/login'
        data = {
            'username': 'admin',
            'password': '123456'
        }
        res = self.key.do_post(url=login_url, json=data).json()
        # 将 token赋值
        Case.token = res['token']
        print(res.text)
        print(self.token)

    def test_02_info(self):
        print('******' + self.token)
        user_url = 'http://127.0.0.1:5000/api/getuserinfo'
        header = {

            "token": self.token
            # 关联内容要做成全局变量
        }
        res1 = self.key.do_get(url=user_url, headers=header).json()
        print(res1.text)
        # Case.openid = res1['data'][0]['openid']
        # Case.userid = res1['userid']
        Case.openid = self.key.get_text(res.text, 'openid')
        Case.userid = self.key.get_text(res.text, 'userid')

    @file_data('../data/add.yaml')  # unnitest 加载数据可以使用 ddt 的file_data
    def test_03_add(self):
        print(self.openid)
        print(self.userid)
        # url=''
        kwargs['headers']['token'] = self.token
        kwargs['data']['userid'] = self.userid
        kwargs['data']['opendid'] = self.opendid
        # data= {}
        res = self.key.do_post(url=kwargs['url'], headers=kwargs['headers'], json=kwargs['data'])
        Case.cartid = self.key.get_text(res.text, 'cartid')

    @file_data('../data/order.yaml')  # unnitest 加载数据可以使用 ddt 的file_data
    def test_04_order(self,**kwargs):
        # url = self.url + kwargs['path']
        # kwargs['headers']['token'] = self.token
        # kwargs['data']['userid'] = self.userid
        # kwargs['data']['opendid'] = self.opendid
        # kwargs['data']['cartid'] = self.cartid
        data= self.assignment(kwargs)
        url=self.url +data['path']
        # data= {}
        # res = self.key.do_post(url=kwargs['url'], headers=kwargs['headers'], json=kwargs['data'])
        # res = self.key.do_post(url=self.url, headers=kwargs['headers'], json=kwargs['data'])
        res = self.key.do_post(url=self.url, headers=data['headers'], json=data['data'])
        print(res.text)
        # 断言 result 是否是 sucess
        self.assertEqual(data['result'], self.key.get_text(res.text,'result'), msg='断言失败')
if __name__ == '__main__':
    unittest.main()
