

import os
import threading
import subprocess
import shlex
import re

# 源文件
path = '/Users/imwallet/Desktop/video/'

# logo文件
path_icon = '/Users/imwallet/Desktop/icon/80.png'

# 输出文件
path_result = '/Users/imwallet/Desktop/resultVideo/'


part_one_list = []
part_two_list = []

def createFileList():

    movie_names = os.listdir(path)
    count = len(movie_names)
    for idx, movie in enumerate(movie_names):
        if idx < count / 2:
            part_one_list.append(movie)
        else:
            part_two_list.append(movie)


def startWaterMark(movieList):

    for movie_name in movieList:
        # 文件名称和后缀名
        (shotname, extension) = os.path.splitext(movie_name)

        if extension == '.mp4' or extension == '.MP4':
            print('current_thread: %s' % threading.current_thread())
            print('current_thread name: %s' % threading.current_thread().name)

            # 源文件路径
            oldPath = path + movie_name
            # 新文件名
            resultName = shotname + '_logo' + extension
            # 新文件存储路径
            resultPath = path + resultName
            bitrate = getVideoInfo(oldPath)
            if isinstance(bitrate, str):
                sub = "ffmpeg -i "+ oldPath + " -acodec copy -b:v "+bitrate+'k -vf "movie=' + path_icon + '[watermark];[in][watermark]overlay=30:30" ' + resultPath + ''
            else:
                sub = "ffmpeg -i "+ oldPath + ' -vf "movie=' + path_icon + '[watermark];[in][watermark]overlay=30:30" ' + resultPath + ''

            # sub = "ffmpeg -i "+ oldPath + " -i " + path_icon + " -filter_complex overlay=30:30 " + resultPath + ''
            # videoresult = subprocess.run(args=sub, shell=True)
            videoresult = subprocess.check_call(args=sub, shell=True)
            if videoresult == 0:
                # 删除旧文件
                os.remove(oldPath)
                # 重命名新文件
                os.rename(resultPath, oldPath)


def getVideoInfo(path):
    shell_cmd = 'ffmpeg -i ' + path
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            lineInfo = bytes.decode(line)
            if 'bitrate' in lineInfo:
                print('~~~~~~split: {}'.format(lineInfo))
                idx = lineInfo.index('bitrate')
                length = len('bitrate:')
                rus = lineInfo[idx+length:]
                print('~~~~~~idx: {}'.format(idx))
                print('~~~~~~length: {}'.format(length))
                print('~~~~~~rus: {}'.format(rus))
                return re.sub('\D', '', rus)
            else:
                print('')
        else:
            print('')



def creatThreads():
    threads = []
    t1 = threading.Thread(target=startWaterMark, name='part_one', args=(part_one_list,))
    threads.append(t1)
    t2 = threading.Thread(target=startWaterMark, name='part_two', args=(part_two_list,))
    threads.append(t2)

    for t in threads:
        # t.setDaemon(True)
        t.start()
    for t in threads:
        threading.Thread.join(t)
        # t.join()
    print('视频logo完成！！')



def watermark():
    movie_names = os.listdir(path)
    for movie_name in movie_names:
        # 文件名称和后缀名
        (shotname, extension) = os.path.splitext(movie_name)

        if extension == '.mp4' or extension == '.MP4':
            # 源文件路径
            oldPath = path + movie_name
            # 新文件名
            resultName = shotname + '_logo' + extension
            # 新文件存储路径
            resultPath = path_result + resultName
            # sub = 'ffmpeg -i ' + oldPath
            # sub = "ffmpeg -i "+ oldPath + " -i " + path_icon + " -filter_complex overlay=30:30 " + resultPath + ''
            bitrate = getVideoInfo(oldPath)
            print('~~~~~~~bitrate: %s', bitrate)
            sub = "ffmpeg -i "+ oldPath + " -acodec copy -b:v "+str(bitrate)+'k -vf "movie=' + path_icon + '[watermark];[in][watermark]overlay=30:30" ' + resultPath + ''
            print('~~~~~~~sub: %s', sub)

            # videoresult = subprocess.call(args=sub, shell=True)
            videoresult = subprocess.run(args=sub, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            # print('videoresult.stdout %s' % videoresult)
            # videoresult = subprocess.check_call(args=sub, shell=True)
            # info = subprocess.check_output(sub)
            # if videoresult == 0:
            #     # 删除旧文件
            #     os.remove(oldPath)
            #     # 重命名新文件
            #     os.rename(resultPath, oldPath)

    print('视频logo完成！！')


if __name__ == '__main__':
    createFileList()
    # print('host_list %s' % part_one_list)
    # print('port_list %s' % part_two_list)
    creatThreads()

    # watermark()
