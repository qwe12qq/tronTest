import os,sys
import json
import requests
import time
import aiohttp
import asyncio
from datetime import datetime

def main():
    url = "https://raw.githubusercontent.com/ellipsis-finance/vecrv-airdrop/master/distributions/distribution-2021-04-08.json"
    res = json.loads(requests.get(url).text)

    for account,value in res["claims"].items():
        index = value["index"]
        amount = value["amount"]
        proof = value["proof"]

        url = "http://123.56.166.152:10088/ssp/getAirDropData?round=1&addr=%s" % (account)
        res = json.loads(requests.get(url).text)
        indexInterface ,amountInterface,proofInterface = res["index"],res["amount"],res["proof"]
        print (index,indexInterface)
        assert index == indexInterface,"index failed!index： %s,indexInterface： %s"%(index,indexInterface)
        assert amount == amountInterface,"amount failed!amount： %s,amountInterface： %s"%(amount,amountInterface)
        assert proof == proofInterface,"proof failed!proof： %s,proofInterface： %s"%(proof,proofInterface)


import aiohttp
import asyncio
import time
from urllib.request import urljoin
import re
import multiprocessing as mp

def parse(res,dict):
    account = dict["account"]
    index = res.get(account).get("index")
    amount = res.get(account).get("amount")
    proof = res.get(account).get("proof")
    res = json.loads(dict["res"])
    # print(res)
    indexInterface, amountInterface, proofInterface = res["data"]["index"], res["data"]["amount"], res["data"]["proof"]
    print (account,index,indexInterface)
    assert index == indexInterface,"index failed!index： %s,indexInterface： %s"%(index,indexInterface)
    assert amount == amountInterface,"amount failed!amount： %s,amountInterface： %s"%(amount,amountInterface)
    assert proof == proofInterface,"proof failed!proof： %s,proofInterface： %s"%(proof,proofInterface)
    return 1

async def crawl(url, session):
    account = url.split("=")[-1]
    r = await session.get(url)
    html = await r.text()
    await asyncio.sleep(0.0001)        # slightly delay for downloading
    dict = {"account":account,"res":html}
    return dict

async def main(loop):
    # url = "https://raw.githubusercontent.com/ellipsis-finance/vecrv-airdrop/master/distributions/distribution-2021-04-08.json"
    # res = json.loads(requests.get(url).text)
    f = open("../data/distribution-2021-06-02.json",'r').read()
    res = json.loads(f)
    url_list =[]
    for account in res["claims"].keys():
        url_list.append("http://123.56.166.152:10088//ssp/getAirDropData?round=1&addr=%s"% (account))
        # url_list.append("https://api.just.network//ssp/getAirDropData?round=1&addr=%s"% (account))

    pool = mp.Pool(10)           #slightly affected
    async with aiohttp.ClientSession() as session:
        print('\nAsync Crawling...')
        tasks = [loop.create_task(crawl(url, session)) for url in url_list]
        finished, unfinished = await asyncio.wait(tasks)
        htmls = [f.result() for f in finished]
        print('\nDistributed Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(res["claims"], html,)) for html in htmls]
        results = [j.get() for j in parse_jobs]

# 使用异步：可以先完成爬虫（异步对爬虫效率提升明显，需要使用aiohttp方式），
# 把结果收集起来，在做结果分析，用多进程的方式进行结果分析
# await 标记切换点
if __name__ == "__main__":
    # main()    # 普通方式
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print("Async total time: ", time.time() - t1)



