# -* coding:utf-8 *- #
# @Time: 2022/3/26 21:17
# @Author:NYH
# @Software:PyCharm
import os
from tqdm import tqdm
import requests, struct

url = 'https://www.pearvideo.com/video_1756378'
countId = url.split('_')[1]
get_url = 'https://www.pearvideo.com/videoStatus.jsp?contId={}'.format(countId)
# print(get_url)
headers = {'Referer': url}
reps = requests.get(url=get_url, headers=headers)
# print(reps.json())
data = reps.json()
src_url = data['videoInfo']['videos']['srcUrl']
systime = data['systemTime']
cur_url = src_url.replace(systime, 'cont-{}'.format(countId))
# print(cur_url)
video_path = './梨视频.mp4'


def down_url(url, file, size):
    with open(file, 'wb') as f:
        reps = requests.get(url=url, stream=True)
        # len = eval(reps.headers['Content-Length'])
        bar = tqdm(desc=file.rsplit('/')[-1], unit='iB', leave=True,
                   total=eval(reps.headers['Content-Length']))
        print('开始下载')
        for chunk in reps.iter_content(chunk_size=size):
            f.write(chunk)
            bar.update(size)
        print('{}, 下载完成'.format(file))
        reps.close()


if __name__ == '__main__':
    down_url(url=cur_url, file=video_path, size=2048)
