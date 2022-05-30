# 线性代码的实现
import requests

login_url = 'http://127.0.0.1:5000/api/login'
data = {
    'username': 'admin',
    'password': '123456'
}
res = requests.post(url=login_url, json=data).json()
token = res['token']
print(res.text)
print(token)
user_url = 'http://127.0.0.1:5000/api/getuserinfo'
header = {

    "token": token
}
res1 = requests.get(url=user_url, headers=header)
print(res1.text)
