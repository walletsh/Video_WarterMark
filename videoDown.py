import os
import re
import json
import requests
from requests import RequestException
from pyquery import PyQuery as pq


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        print('~~~~headers~~~~{}'.format(response.headers))
        if response.status_code == 200:
            print('~~~~text~~~~'.format(response.text))
            return response.text
        return None
    except RequestException:
        return None


def parse_page(html):
    doc = pq(html)
    items = doc('.url').items()
    for item in items:
        yield item.text()


def get_real_url(url, try_count=1):
    if try_count > 3:
        return None
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code >= 400:
            return get_real_url(url, try_count + 1)
        return response.url
    except RequestException:
        return get_real_url(url, try_count + 1)


def get_m3u8_url(url):
    try:
        path_pattern = re.compile('(\d+)', re.S).search(url).group(1)
        get_play_url = 'https://lens.zhihu.com/api/videos/' + path_pattern
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        content = requests.get(get_play_url, headers=headers).text
        data = json.loads(content)  # 将json格式的字符串转化为字典
        if data and 'playlist' in data.keys():
            m3u8_url = data.get('playlist').get('sd').get('play_url')
            return m3u8_url
    except Exception:
        return None


def get_m3u8_content(url, try_count=1):
    if try_count > 3:
        print('Get M3U8 Content Failed', url)
        return None
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        return get_m3u8_content(url, try_count + 1)
    except RequestException:
        return get_m3u8_content(url, try_count + 1)


def get_ts(url, try_count=1):
    if try_count > 3:
        print('Get TS Failed', url)
        return None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        return get_ts(url, try_count + 1)
    except RequestException:
        return get_ts(url, try_count + 1)


def download_ts(m3u8_url, video_url, video_count):
    print('准备下载', video_url)
    download_path = '/Users/imwallet/Desktop/video/'
    try:
        all_content = get_m3u8_content(m3u8_url)
        print('~~~~~~~~~all_content~~~~~~~~~~~ {}'.format(all_content))
        file_line = all_content.split('\n')  # 读取文件里的每一行
        print('~~~~~~~~~file_line~~~~~~~~~~~ {}'.format(file_line))

        # 通过判断文件头来确定是否是M3U8文件
        if file_line[0] != '#EXTM3U':
            raise BaseException('非M3U8链接')
        else:
            unknow = True  # 用来判断是否找到了下载的地址
            for index, line in enumerate(file_line):
                if "EXTINF" in line:
                    unknow = False
                    # 拼出ts片段的URL
                    pd_url = m3u8_url.rsplit('/', 1)[0] + '/' + file_line[index + 1]  # rsplit从字符串最后面开始分割
                    response = get_ts(pd_url)
                    c_fule_name = str(file_line[index + 1]).split('?', 1)[0]
                    source_path = c_fule_name.split('-', 1)[0]  # 区分不同源的视频流
                    print('正在下载', c_fule_name)
                    with open(download_path + c_fule_name, 'wb') as f:
                        f.write(response.content)
                        f.close()
            if unknow:
                raise BaseException('未找到对应的下载链接')
            else:
                print('下载完成，准备合并视频流...')
                merge_file(download_path, source_path, video_count)
    except Exception:
        print('~~~~~~~~faile~~~~~~~~~')
        return None


def merge_file(download_path, source_path, video_count):
    os.chdir(download_path)  # 修改当前工作目录
    merge_cmd = 'copy /b ' + source_path + '*.ts video' + str(video_count) + '_' + source_path + '.mp4'
    split_cmd = 'del /Q ' + source_path + '*.ts'
    os.system(merge_cmd)
    os.system(split_cmd)


def main():
    url = 'https://v.vzuu.com/video/1059570887484817408'  # 含有知乎小视频的链接
    html = get_page(url)
    print('html: '.format(html))
    video_count = 0
    if html:
        video_urls = parse_page(html)
        for video_url in video_urls:
            if video_url:
                real_url = get_real_url(video_url)
                if real_url:
                    print('~~~~~real_url~~~~~')
                    m3u8_url = get_m3u8_url(real_url)
                    if m3u8_url:
                        video_count += 1
                        download_ts(m3u8_url, video_url, video_count)


if __name__ == '__main__':
    main()

