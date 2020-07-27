import qrcode
import os
import sys
import shutil
import requests

# ====================================== robot ===================================
'''
微信群机器人测试，使用前先设置 __hook_url

'''

# 群机器人 hook url
__hook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9d8617dd-444d-41a0-9851-d96dec337677'


def build_text_msg(content):
    '''
    构造文本消息
    {
    'msgtype': 'text',
    'text': {
        'content': '广州今日天气：29度，大部分多云，降雨概率：60%',
        'mentioned_list':['wangqing','@all'], // userid 列表，@all 表示提醒所有人
        'mentioned_mobile_list':['13800001111','@all'] // 手机号列表
        }
    }

    :param content: 文本内容，2048字节内，utf-8 编码
    :return: 文本消息 dict
    '''
    return {
        'msgtype': 'text',
        'text': {
            'content': content
        }
    }


def build_new_msg(articles):
    '''
    构造图文类型的消息
    https://work.weixin.qq.com/help?person_id=1&doc_id=13376

    {
    'msgtype': 'news',
    'news': {
       'articles' : [
           {
               'title' : '中秋节礼品领取',
               'description' : '今年中秋节公司有豪礼相送',
               'url' : 'URL',
               'picurl' : 'http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png'
           }
        ]
        }
    }


    :param articles: [{'title':'','description':'','url':'','picurl':''}]
    数组，最多 8个，title 128字节以内， description 512 字节以内

    :return:
    '''

    return {
        'msgtype': 'news',
        'news': {
            'articles': articles
        }
    }


def send_text_msg(content):
    '''
    发送文本下消息

    :param content:
    :return:
    '''
    send_msg(build_text_msg(content))


def send_news_msg(content):
    '''
    发送图文消息

    :param content:
    :return:
    '''
    send_msg(build_new_msg(content))


def send_msg(msg):
    '''
    发送消息

    :param content:
    :return:
    '''
    headers = {
        'user-agent': 'jenkins'
    }
    r = requests.post(__hook_url, json=msg, headers=headers)
    if r.status_code == 200:
        print('消息发送成功')
    else:
        print('消息发送失败')


# ====================================== apk =======================================

__src_dir = 'app/build/outputs/apk/'
__dst_dir = 'apks/'


def ensure_dirs():
    if os.path.exists(__dst_dir):
        return
    os.mkdir(__dst_dir)


def find_apks(result, dir=__dst_dir):
    '''
    find apk from dir

    :param result: 数组
    :param dir:
    :return:
    '''
    for f in os.listdir(dir):
        apk_file = os.path.join(dir, f)
        if os.path.isdir(apk_file):
            find_apks(result, apk_file)
        elif f.endswith('.apk'):
            result.append(apk_file)


def move_apks(apk_list):
    '''
    将 apk 移动到指定位置

    :param apk_list:
    :return:
    '''
    if len(apk_list) > 0:
        for apk in apk_list:
            shutil.move(apk, __dst_dir)


def gen_qr_code(url, dst):
    '''
    使用 url 生成二维码

    :param url:
    :param dst: 二维码保存路径
    :return:
    '''
    img = qrcode.make(url)
    img.save(dst)


def build(args):
    cmd = r'gradlew clean assembleDebug'
    r = os.system(cmd)
    print('command result {0}', r)

    job_url = args[1]  # jenkins job url
    job_num = args[2]  # jenkins job num

    if r == 0:
        print('================= gradle build success! =======================')
        # apk 列表
        apk_list = []
        find_apks(apk_list, __src_dir)
        print(apk_list)

        # jenkins job url
        print('args: ')
        print(args)

        articles = []  # 消息列表

        for f in apk_list:
            pic_path = '{0}.png'.format(f[:-4])  # 二维码保存路径
            apk_url = job_url + f  # apk url
            gen_qr_code(apk_url, pic_path)  # 生成二维码
            pic_url = job_url + pic_path  # 图片 url

            # 构造一个消息
            d = {
                'title': job_num,
                'description': '打包成功',
                'url': apk_url,
                'picurl': pic_url
            }
            articles.append(d)

        # 发送消息
        print('================== 开始发送消息 =========================')
        send_news_msg(articles)

    else:
        # 发送失败消息
        msg = '{0} 打包失败'.format(job_num)
        send_text_msg(msg)


if __name__ == '__main__':
    build(sys.argv)
