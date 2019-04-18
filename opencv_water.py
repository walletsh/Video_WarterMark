
import cv2
import numpy as np
from ffmpy import FFmpeg
import sys
import ffmpeg
import subprocess
import shlex
import re

# 源文件
path = '/Users/imwallet/Desktop/video/1542334461889205_1542357171131981_1544081678098615.mp4'

# logo文件
path_icon = '/Users/imwallet/Desktop/icon/'

# 输出文件
path_result = '/Users/imwallet/Desktop/resultVideo/'

def po():
    shell_cmd = 'ffmpeg -i ' + path
    cmd = shlex.split(shell_cmd)
    print('shell_cmd: {}'.format(shell_cmd))
    print('cmd: {}'.format(cmd))

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
                # split = lineInfo.split(',')
                # print('~~~~~~split: {}'.format(split))
                # for content in split:
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')



    # for i in iter(p.stdout.readline, b''):
    #     print('~~~~~~~' + i.rstrip())

    # returncode = p.poll()
    # while returncode is None:
    #     print('~~%s' % p.stdout.readline().strip())
    #     returncode = p.poll()
    # print('`````````%s' % p.stdout.read())
    # print('$$$%s' % returncode)



def ffmpeg_out():
    # probe = FFmpeg(path)
    #
    # print(probe.executable)
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe.process['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        sys.exit(1)
    # 宽度
    width = int(video_stream['width'])
    # 高度
    height = int(video_stream['height'])
    # 帧数
    num_frames = int(video_stream['nb_frames'])
    # 时长
    time = (video_stream['duration'])
    # 比特率
    bitrate = (video_stream['bit_rate'])

    print('width: {}'.format(width))
    print('height: {}'.format(height))
    print('num_frames: {}'.format(num_frames))
    print('time: {}'.format(time))
    print('bitrate: {}'.format(bitrate))




def waterMark_opencv():
    matimage = cv2.imread(path_icon + '80.png')
    matimagenew = matimage - matimage
    watermark_template_filename = path_icon + '80.png'
    matlogo = cv2.imread(watermark_template_filename)
    matimagenew[359:359 + matlogo.shape[0], 453:453 + matlogo.shape[1]] = matlogo
    imagenew = cv2.addWeighted(matimage, 1, matimagenew, 1, 1)
    savepath = path + '20180516144933.png'
    cv2.imwrite(savepath,imagenew)



if __name__ == '__main__':
    po = po()
    print('po: {}'.format(po))
    # ffmpeg_out()

