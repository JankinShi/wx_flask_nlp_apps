# -*- coding:utf-8-*-
import requests
import itchat


class Ot_robot:
    def __init__(self):
        self.headers = {'content-type': 'application/json'}  # 出于习惯加上的请求头，可无

    def ot_chat(self, text):
        # 获取思知机器人的回复信息
        data = {
            "appid": "填自己的",
            "userid": "填自己的",
            "spoken": text,
        }
        url = 'https://api.ownthink.com/bot'  # API接口
        response = requests.post(url=url, data=data, headers=self.headers)
        response.encoding = 'utf-8'
        result = response.json()
        answer = result['data']['info']['text']
        print(answer)
        return answer


#本模块测试
if __name__ == '__main__':
    while True:
        robot = Ot_robot() # instance
        text = input('主人说：')
        if text == 'Q':
            break
        robot.ot_chat(text=text)

