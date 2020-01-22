import requests
import json
import re
import urllib.request

from .settings import TULING_API_KEY, TULING_UER_ID


class Robot:
    def __init__(self):
        self.api = 'http://openapi.tuling123.com/openapi/api/v2'
        # self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0',
        #                'Accept': 'application / json, text / javascript, * / *; q = 0.01'
        #                }
        self.header = {'content-type': 'application/json'}

    def chat1(self,message):
        req = {
            "reqType": 0,  # 输入类型 0-文本, 1-图片, 2-音频
            "perception":  # 信息参数
                {
                    "inputText":  # 文本信息
                        {
                            "text": message
                        },

                    "selfInfo":  # 用户参数
                        {
                            "location":
                                {
                                    "city": "深圳",  # 所在城市
                                    "province": "广东",  # 省份
                                    "street": "红花岭路"  # 街道
                                }
                        }
                },
            "userInfo":
                {
                    "apiKey": TULING_API_KEY,  # 改为自己申请的key
                    "userId": TULING_UER_ID  # 用户唯一标识(随便填, 非密钥)
                }
        }
        # 将字典格式的req编码为utf8
        req = json.dumps(req).encode('utf8')
        http_post = urllib.request.Request(url=self.api, data=req, headers=self.header)
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        response_dic = json.loads(response_str)

        print('response_dic :', response_dic)
        results_text = response_dic['results'][0]['values']['text']
        print('first result:', results_text)
        return results_text
        # data_strs = re.findall(r"'results'.*'values': {'text': '(.*?)'",data_str,re.S)
        # for i in range(len(data_strs)):
        #     print(data_strs[i])
        #     yield data_strs[i]



        # intent_code = response_dic['intent']['code']
        # results_text = response_dic['results'][0]['values']['text']
        # print('机器人1号：', results_text)
        # return results_text

    # def chat(self,message):
    #     form ={
    #                 "perception": {
    #                     "inputText": {
    #                         "text": str(message)
    #                                  }
    #                                },
    #                 "userInfo":{
    #                     "apiKey":TULING_API_KEY,
    #                     "userId": TULING_UER_ID}  # 用户唯一标识(随便填, 非密钥)
    #                 }
    #
    #     json_data = json.dumps(form)
    #
    #     response = requests.post(url=self.api,data=json_data,headers =self.header)
    #
    #     data_str = str(response.json())
    #     print('data_str :', data_str)
    #     data_strs = re.findall(r"'results'.*'values': {'text': '(.*?)'",data_str,re.S)
    #     for i in range(len(data_strs)):
    #         yield data_strs[i]
    #
    #     data_url = re.findall(r"'results'.*'values': {'url': '(.*?)'", data_str, re.S)
    #     for m in range(len(data_url)):
    #         yield data_url[m]
#本模块测试
if __name__ == '__main__':
    while True:
        robot = Robot() # instance
        text = input('主人说：')
        if text == 'Q':
            break
        robot.chat1(message=text)





