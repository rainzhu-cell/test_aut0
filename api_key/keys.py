import json

import jsonpath
import requests
from wx.lib.pubsub.core import kwargs


class Key:
    # get 请求
    def do_get(self, url, params=None, **kwargs):
        return requests.get(url=url, params=params, **kwargs)

    # post 请求
    def do_post(self, url, data=None, **kwargs):
        return requests.post(url=url, params=data, **kwargs)

    # 获取响应结果中指定的value值

    def get_text(self, text, key):
        try:
            temp = json.loads(text)
            value = jsonpath.jasonpath(temp, '$..{}'.format(key))
            # jsonpath 返回的结果是list
            if len(value) == 1:
                return value[0]
                return value
        except Exception as  e:
            print(e)
            return None
