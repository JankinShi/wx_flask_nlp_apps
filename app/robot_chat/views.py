# 蓝本中的路由和视图函数
from flask import render_template, redirect, request, url_for, flash,current_app
import hashlib
from . import robot_chat
from flask import jsonify,json
from . import receive
from . import reply

from wechatpy import parse_message, WeChatClient
# from wechatpy.replies import TextReply, ImageReply, VoiceReply, MusicReply
from . import tulingrobot  #  图灵机器人
from . import own_think_robot  # 思知机器人


@robot_chat.route('/test',methods=['GET','POST'])
def test():
    if request.method == "GET":  # 判断请求方式是GET请求
        return 'this is test'

@robot_chat.route('/wx',methods=['GET','POST'])
def wx():
    if request.method == "GET":  # 判断请求方式是GET请求
        my_signature = request.args.get('signature')  # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        token = 'jankin'
        # 进行字典排序
        data = [token, my_timestamp, my_nonce]
        data.sort()
        # 拼接成字符串
        temp = ''.join(data)
        # 进行sha1加密
        mysignature = hashlib.sha1(temp.encode('utf8')).hexdigest()
        # 加密后的字符串可与signature对比，标识该请求来源于微信
        print('开始验证中')
        if my_signature == mysignature:
            print("验证成功：", my_echostr)
            return my_echostr
        else:
            return '微信后台验证失败'

        #  如果是post请求代表微信给我们把用户消息转发过来了
    if request.method == "POST":
        dt = request.data
        print("Handle Post webdata is ", dt)
        # 后台打日志
        recMsg = receive.parse_xml(dt)
        print('xml_recMsg.MsgType is :', recMsg.MsgType)
        if recMsg.MsgType == 'text':  #isinstance(recMsg, receive.Msg) and
            toUser = str(recMsg.FromUserName)
            fromUser = str(recMsg.ToUserName)
            # content = "test"
            # print('toUser is :', toUser)
            # print('fromUser is :', fromUser)
            # print('content is :', content)

            robot = own_think_robot.Ot_robot()
            own_think_msgs = robot.ot_chat(recMsg.Content)  # 获得问答结果
            replyMsg = reply.TextMsg(toUser, fromUser, own_think_msgs)
            # print('reply已经实例化')
            return replyMsg.send()

        else:
            print('未处理')
            return "success"

        # print('post:',"用户开始发送消息")
        # xml = request.data
        # print('weiixn_xml:', xml)
        # msg = parse_message(xml)
        # 文本信息
        # if msg.type == 'text':
        #     return 'hello!!!'
            # robot = Robot()
            # tuling_msgs = robot.chat(msg.Content)
            # msg_data = ''
            # for tuling in tuling_msgs:
            #     msg_data += tuling
            # reply = TextReply(content=msg_data, message=msg)
            # xml = reply.render()
            # return xml
        # #  图片信息
        # elif msg.type == 'image':
        #     name = img_download(msg.image, msg.source)
        #     print(IMAGE_DIR + name)
        #     r = access_api(IMAGE_DIR + '/' + name)
        #     if r == 'success':
        #         media_id = img_upload(msg.type, FACE_DIR + '/' + name)
        #         reply = ImageReply(media_id=media_id, message=msg)
        #     else:
        #         reply = TextReply(content='人脸检测失败，请上传1M以下人脸清晰的照片', message=msg)
        #     xml = reply.render()
        #     return xml
        # #  语音消息
        # elif msg.type == 'voice':
        #     reply = VoiceReply(media_id=msg.media_id, message=msg)
        #     xml = reply.render()
        #     return xml
        #
        # else:
        #     reply = TextReply(content='抱歉，功能构建中', message=msg)
        #     xml = reply.render()
        #     return xml


def create_menu(request):
	# 第一个参数是公众号里面的appID，第二个参数是appsecret
    client = WeChatClient("wxd8adb366cf6afb91", "4c0faa3a007df74b0664da87ad2887b8")
    client.menu.create({
         "button": [
            {
                "type": "click",
                "name": "今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "type": "click",
                "name": "歌手简介",
                "key": "V1001_TODAY_SINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ],
        "matchrule": {
            "group_id": "2",
            "sex": "1",
            "country": "中国",
            "province": "广东",
            "city": "广州",
            "client_platform_type": "2"
        }
    })
    return 'ok'
    # return HttpResponse('ok')