# 蓝本中的路由和视图函数
from flask import render_template, redirect, request, url_for, flash,current_app
import hashlib
from . import couplets
from flask import Flask
from flask import jsonify,json
from .model import Model

from wechatpy.utils import check_signature
from wechatpy import parse_message
from wechatpy.exceptions import InvalidSignatureException
# from wechatpy.replies import TextReply, ImageReply, VoiceReply, MusicReply



@couplets.route('/cps', methods=['GET', 'POST'])
def get_couplets():
    try:
        t_result = {'a':'wanna couplets?'}
    finally:
        pass
    jsonList = json.dumps(t_result)

    return jsonList


@couplets.route('/wx/couplets',methods=['GET','POST'])
def wx():
    if request.method == "GET":  # 判断请求方式是GET请求
        # try:
        #     my_signature = request.args.get('signature')  # 获取携带的signature参数
        #     my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
        #     my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
        #     my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        #     token = 'jankin'
        #     check_signature(token, my_signature, my_timestamp, my_nonce)
        # except InvalidSignatureException:

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
            return my_echostr
        else:
            return '微信后台验证失败'
         # 如果是post请求代表微信给我们把用户消息转发过来了
    if request.method == "POST":
        xml = request.data
        msg = parse_message(xml)
        # 文本信息
        if msg.type == 'text':
            return 'hello!!!'
            # robot = Robot()
            # tuling_msgs = robot.chat(msg.content)
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


vocab_file = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/vocabs.txt'
model_dir = 'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/output_model/output_couplet'

m = Model(
        None, None, None, None, vocab_file,
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.0001,
        output_dir=model_dir,
        restore_model=True, init_train=False, init_infer=True)


@couplets.route('/couplet/<in_str>', methods=['GET', 'POST'])
def chat_couplet(in_str):
    if len(in_str) == 0 or len(in_str) > 50:
        output = u'您的输入太长了'
    else:
        output = m.infer(' '.join(in_str))
        output = ''.join(output.split(' '))
    print('上联：%s；下联：%s' % (in_str, output))
    return jsonify({'output': output})

