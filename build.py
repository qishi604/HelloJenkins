import qrcode
import os
import shutil

__src_dir = 'app/build/outputs/apk/'
__dst_dir = 'apks/'


def ensure_dirs():
    if not os.path.exists(__dst_dir):
        os.mkdir(__dst_dir)


def find_apks(result, dir=__dst_dir):
    """
    find apk from dir

    :param result: 数组
    :param dir:
    :return:
    """
    for f in os.listdir(dir):
        apk_file = dir + os.sep + f
        if os.path.isdir(apk_file):
            find_apks(result, apk_file)
        elif f.endswith('.apk'):
            result.append(apk_file)


def move_apks(apk_list):
    """
    将 apk 移动到指定位置

    :param apk_list:
    :return:
    """
    if len(apk_list) > 0:
        for apk in apk_list:
            shutil.move(apk, __dst_dir)


def gen_qr_code(url, dst):
    """
    使用 url 生成二维码

    :param url:
    :param dst: 二维码保存路径
    :return:
    """
    img = qrcode.make(url)
    img.save(dst)


def build():
    cmd = r'gradlew clean assembleDebug'
    r = os.system(cmd)
    print('command result {0}', r)
    if r == 0:
        print('build success!')
        ensure_dirs()
        apks_list = []
        find_apks(apks_list, __src_dir)
        move_apks(apks_list)
        apks_list = []
        find_apks(apks_list)
        print(apks_list)

        for f in apks_list:
            dst_name = '{0}.png'.format(f[:-4])
            gen_qr_code(f, dst_name)


if __name__ == '__main__':
    build()
