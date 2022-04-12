# -* coding:utf-8 *- #
# @Time: 2022/3/26 20:28
# @Author:NYH
# @Software:PyCharm
import time, asyncio, aiohttp, aiofiles
from concurrent.futures import ThreadPoolExecutor

now = time.strftime("%Y-%m-%d")
url = 'http://www.xinfadi.com.cn/getPriceData.html'


async def down_price(pageNum, session):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               }
    data = {
        'limit': 20,
        'current': pageNum
    }
    # async with aiohttp.ClientSession() as session:
    async with session.post(url=url, data=data, headers=headers) as reps:
        datas = await reps.json()
        datas = datas['list']
        # print((datas, type(datas)))
    async with aiofiles.open(f'{now}菜价.csv', 'a+', encoding='utf8') as f:
        await f.write('品名\t')
        await f.write('最低价\t')
        await f.write('最高价\t')
        await f.write('均价\t')
        await f.write('单位\t')
        await f.write('日期\n')
        for data in datas:
            # print(data)
            await f.write(f"{data['prodName']}\t")
            await f.write(f"{data['lowPrice']}\t")
            await f.write(f"{data['highPrice']}\t")
            await f.write(f"{data['avgPrice']}\t")
            await f.write(f"{data['unitInfo']}\t")
            await f.write(f"{data['pubDate']}\n")
    print(f'第{pageNum}页数据提取完毕')


async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 20):
            tasks.append(asyncio.create_task(down_price(i, session)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    print('**********开始请求今日菜价数据***********')
    t1 = time.time()
    with ThreadPoolExecutor(50) as t:
            t.submit(asyncio.run(main()))
    t2 = time.time()
    print(t2 - t1)
    print('***********请求完毕！*************')
