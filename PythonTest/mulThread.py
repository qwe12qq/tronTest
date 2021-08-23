import os,sys
import json
import threading
import requests
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor,as_completed

def crawl_spider(url):
    s = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
    try:
        content = requests.get(url, headers=headers)
        if (content.status_code == 200):
            s = content.text
            resQueue.put(s)
    except Exception as e:
        print('采集线程错误',e)
    return s

def parse(res):
    f.write(res + "\n")

def close():
    f.close()

resQueue = Queue()
f = open("res","w")
# def main():
#     pageQueue = Queue()
#     thread_list = []
#     for page in range(1,21):
#         pageQueue.put(page)
#     while True:
#         if pageQueue.empty():
#             break
#         page = pageQueue.get()
#         url = 'http://127.0.0.1:5000/demo?p={}'.format(str(page))
#         m = threading.Thread(target=crawl_spider, args=(url,))
#         m.start()
#         thread_list.append(m)
#     for m in thread_list:
#         m.join()
#
#     list = []
#     while True:
#         if resQueue.empty():
#             break
#         res = resQueue.get()
#         t = threading.Thread(target=parse,args=(res,))
#         t.start()
#         list.append(t)
#     for t in list:
#         t.join()

def main():
    pageQueue = Queue()
    for page in range(1,10000):
        pageQueue.put(page)
    url_list = []
    while True:
        if pageQueue.empty():
            break
        page = pageQueue.get()
        url_list.append('http://127.0.0.1:5000/demo?p={}'.format(str(page)))
    executor = ThreadPoolExecutor(max_workers=100)
    for data in executor.map(crawl_spider, url_list):  #data 是按照url_list顺序放置的
        parse(data)

    # with ThreadPoolExecutor(max_workers=30) as t:
    #     obj_list = []
    #     for url in url_list:
    #         obj = t.submit(crawl_spider, url)
    #         obj_list.append(obj)

    # with ThreadPoolExecutor(max_workers=150) as t:
    #     while True:
    #         if resQueue.empty():
    #             print ("stop...")
    #             break
    #         res = resQueue.get()
    #         obj_list = []
    #         obj = t.submit(parse, res)
    #         obj_list.append(obj)

if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print (e-s)
    close()



import aiohttp
import asyncio
from datetime import datetime


async def fetch1(client,page):
    # print("打印 ClientSession 对象")
    async with client.get('http://127.0.0.1:5000/demo?p={}'.format(str(page))) as resp:
        assert resp.status == 200
        text = await resp.text()

async def fetch(page,semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:5000/demo?p={}'.format(str(page))) as resp:
                assert resp.status == 200
                text = await resp.text()
                result.append(text)


async def main(result):
    start = datetime.now()
    print(start)
    # async with aiohttp.ClientSession() as client:
        # tasks = []
        # for i in range(1,20000):
        #     tasks.append(asyncio.create_task(fetch(client,i)))
        # await asyncio.wait(tasks)

    semaphore = asyncio.Semaphore(100)
    to_get = [fetch(i, semaphore) for i in range(10000)]
    await asyncio.wait(to_get)
    f= open("res",'w')
    f.write('\n'.join(result))
    end = datetime.now()
    print("aiohttp版爬虫花费时间为：")
    print(end - start)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = []
    loop.run_until_complete(main(result))


