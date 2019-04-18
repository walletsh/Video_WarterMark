
import os
import requests

def do_load_media(url, path):
    try:
        # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                print('~~~~~~~~exists~~~~~~~~')
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            response = requests.get(url, stream=True, headers=headers)
            print('~~~~~~~~ no exists status_code~~~~~~~~ {}'.format(response.status_code))
            print('~~~~~~~~ no exists headers~~~~~~~~ {}'.format(response.headers))
            response.encoding = 'utf-8'
            con = response.text
            print(con)

            content_length = int(response.headers['content-length'])
            print('content_length %s' % content_length)
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                print('~~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~')
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                print('open content_length %s' % content_length)
                file.write(response.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print('error {}'.format(e))
        print('repr(e):\t', repr(e))



def load_media():
    # https://v.vzuu.com/video/1059570887484817408
    url = 'https://vdn1.vzuu.com/SD/11a8c7c8-052a-11e9-9c33-0a580a45fbf6.mp4?disable_local_cache=1&bu=com&expiration=1545966792&auth_key=1545966792-0-0-a3787d060f779e690e81cb07101449f9&f=mp4&v=hw'
    path = r'/Users/imwallet/Desktop/resultVideo/xiaovideo.mp4'
    do_load_media(url, path)
    pass


def main():
    load_media()
    pass


if __name__ == '__main__':
    main()
