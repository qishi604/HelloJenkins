import qrcode
import os
import shutil

__src_dir = 'app/build/outputs/apk/'
__dst_dir = 'apks/'
__qrcode_dir = 'qrcode/'


def move_apks():
    src_dir = __src_dir
    dst_dir = __dst_dir
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            shutil.move(f, dst_dir)
            print('move {0} to {1}', f, dst_dir)
        print('move apks end!')
    else:
        print('{0} not exist'.format(src_dir))


def find_apks(result, dir=__dst_dir):
    """
    find apk from dir

    :param result: 数组
    :param dir:
    :return:
    """
    for f in os.listdir(dir):
        if os.path.isdir(dir):
            find_apks(result, f)
        elif f.endswith('.apk'):
            result.append(f)


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
    cmd = r'gradle clean assembleDebug'
    r = os.system(cmd)
    print('command result')
    print(r)
    if r == 0:
        print('build success!')
        move_apks()
        apks_list = []
        find_apks(apks_list)
        print(apks_list)

        for f in apks_list:
            dst_name = '{0}{1}.png'.format(__dst_dir, f[:-4])
            gen_qr_code(f, dst_name)


if __name__ == '__main__':
    build()
