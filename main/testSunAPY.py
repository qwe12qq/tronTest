import os,sys
import requests
import json

justswap_lp_address_speed = {"TNCXhHpfNjd6Gd3ACCJr9xSm8ZPEgk18KT":{"TRX":390496,"JST":260331,"BTT":8330579,"WIN":31239669,"SUN":868},"TKmuLS7nxiJNZdpQsjKfQHN5Nm32HQa74R":{"TRX":390496,"JST":260331,"BTT":8330579,"WIN":31239669,"SUN":868},"TAtdEkhyqNztNXP6uGD5DTxw4B4GM7RR9N":{"TRX":260331,"JST":173554,"BTT":5553719,"WIN":20826446,"SUN":579},"TQ4WHKwjTiW2FVwbfQzKCg2X5He616ofxY":{"TRX":130165,"JST":86777,"BTT":2776860,"WIN":10413223,"SUN":289},"TFjfWDs7SPbSYMCfD2ch7Ngr7u8RVcgn1d":{"TRX":650826,"JST":433884,"BTT":13884298,"WIN":52066116,"SUN":1446},"TLGmDvkVn6kNXqEegurePabQ4pe5VBH4Xx":{"TRX":650826,"JST":433884,"BTT":13884298,"WIN":52066116,"SUN":1446},"TBjvtyxcng4XNnBvVTxUhJ8LkoBFpTHSss":{"TRX":260331,"JST":173554,"BTT":5553719,"WIN":20826446,"SUN":579},"TVbCsgstN5H59cJpZexjR44juAio3LkD7J":{"TRX":130165,"JST":86777,"BTT":2776860,"WIN":10413223,"SUN":289}}

lend_lp_address_speed = {"TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu":{"TRX":334711,"JST":223140,"BTT":7140496,"WIN":26776860,"SUN":744},"TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA":{"TRX":223140,"JST":148760,"BTT":4760331,"WIN":17851240,"SUN":496},"TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK":{"TRX":334711,"JST":223140,"BTT":7140496,"WIN":26776860,"SUN":744},"TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i":{"TRX":74380,"JST":49587,"BTT":1586777,"WIN":5950413,"SUN":165},"TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ":{"TRX":148760,"JST":99174,"BTT":3173554,"WIN":11900826,"SUN":331},"TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs":{"TRX":148760,"JST":99174,"BTT":3173554,"WIN":11900826,"SUN":331},"TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj":{"TRX":223140,"JST":148760,"BTT":4760331,"WIN":17851240,"SUN":496},"TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz":{"TRX":74380,"JST":49587,"BTT":1586777,"WIN":5950413,"SUN":165},"TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs":{"TRX":74380,"JST":49587,"BTT":1586777,"WIN":5950413,"SUN":165}}


def askrequests(url):
    res = requests.get(url)
    return json.loads(res.text)

def getlpprice(content,flag):
    name = flag + "_lp_address_speed"
    lp_address_speed = eval(name)
    dict = {}
    print (lp_address_speed)
    for lp in lp_address_speed.keys():
        dict[lp] = {"TRX":0,"SUN":0,"JST":0,"BTT":0,"WIN":0}
        for key in dict[lp].keys():
            dict[lp][key] = content["data"].get(lp).get(key).get("price")
    return dict

def parse_apy(apyRes,flag):
    name = flag + "_lp_address_speed"
    lp_address_speed = eval(name)
    dict = {}
    for lp in lp_address_speed.keys():
        dict[lp] = {"TRX":0,"SUN":0,"JST":0,"BTT":0,"WIN":0}
        for key in dict[lp].keys():
            dict[lp][key] = apyRes["data"].get(lp).get(key)
    return dict
# 每个Token的APY计算公式=（矿池每秒产出Token数量 x Token价格 x 31536000 ）/ 当前矿池质押量
def calApy(lpTvlDict,priceDict,flag):
    name = flag + "_lp_address_speed"
    lp_address_speed = eval(name)
    dict = {}
    for lp in lpTvlDict.keys():
        dict[lp] = {"TRX":0,"SUN":0,"JST":0,"BTT":0,"WIN":0}
        for key in dict[lp].keys():
            if lpTvlDict[lp] == 0:continue
            price = float(priceDict[lp][key])
            speed = lp_address_speed[lp][key]/3600/24
            apy = speed*31536000*price/lpTvlDict[lp]
            dict[lp][key] = "%.8f" % apy
    return  dict

def judgment(calculateApyDict,apyDict):
    keys = ["TRX","SUN","JST","BTT","WIN"]
    for lp in calculateApyDict.keys():
        if len(calculateApyDict) != len(apyDict):
            print (lp,"长度不等")
            continue
        for key in keys:
            if float(calculateApyDict[lp][key]) - float(apyDict[lp][key]) > 0.0001:
                print (lp , key ,calculateApyDict[lp][key],apyDict[lp][key])

# APY计算
# http://123.56.166.152:10088/sunProject/tronbull?pool=[用逗号分隔的矿池地址]&tv=[用逗号分割的tvl]

def main():
    #justswap  LP 价格获取接口
    print ("justswap starting.....................")
    url = "http://123.56.166.152:10088/sunProject/tronbullish?pool=TNCXhHpfNjd6Gd3ACCJr9xSm8ZPEgk18KT,TKmuLS7nxiJNZdpQsjKfQHN5Nm32HQa74R,TAtdEkhyqNztNXP6uGD5DTxw4B4GM7RR9N,TQ4WHKwjTiW2FVwbfQzKCg2X5He616ofxY,TFjfWDs7SPbSYMCfD2ch7Ngr7u8RVcgn1d,TLGmDvkVn6kNXqEegurePabQ4pe5VBH4Xx,TBjvtyxcng4XNnBvVTxUhJ8LkoBFpTHSss,TVbCsgstN5H59cJpZexjR44juAio3LkD7J&addr=TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"

    res = askrequests(url)
    price_dict = getlpprice(res,"justswap")
    lp_tvl_dict = {"TNCXhHpfNjd6Gd3ACCJr9xSm8ZPEgk18KT":5110538.39,"TKmuLS7nxiJNZdpQsjKfQHN5Nm32HQa74R":24037.33,"TAtdEkhyqNztNXP6uGD5DTxw4B4GM7RR9N":0,"TQ4WHKwjTiW2FVwbfQzKCg2X5He616ofxY":0,"TFjfWDs7SPbSYMCfD2ch7Ngr7u8RVcgn1d":2177270.74,"TLGmDvkVn6kNXqEegurePabQ4pe5VBH4Xx":66.19,"TBjvtyxcng4XNnBvVTxUhJ8LkoBFpTHSss":22,"TVbCsgstN5H59cJpZexjR44juAio3LkD7J":0.04}
    calculateApyDict = calApy(lp_tvl_dict,price_dict,"justswap")
    url ="http://123.56.166.152:10088/sunProject/tronbull?pool=TNCXhHpfNjd6Gd3ACCJr9xSm8ZPEgk18KT,TKmuLS7nxiJNZdpQsjKfQHN5Nm32HQa74R,TAtdEkhyqNztNXP6uGD5DTxw4B4GM7RR9N,TQ4WHKwjTiW2FVwbfQzKCg2X5He616ofxY,TFjfWDs7SPbSYMCfD2ch7Ngr7u8RVcgn1d,TLGmDvkVn6kNXqEegurePabQ4pe5VBH4Xx,TBjvtyxcng4XNnBvVTxUhJ8LkoBFpTHSss,TVbCsgstN5H59cJpZexjR44juAio3LkD7J&tvl=5110538.39,24037.33,0,0,2177270.74,66.19,22,0.04"
    apy_res = askrequests(url)
    apyDict = parse_apy(apy_res,"justswap")
    print ("计算：",calculateApyDict)
    print("接口：",apyDict)
    judgment(calculateApyDict,apyDict)
    # #################justswap LP 矿池 ending#############
    print ("justswap over......................")

    #lend矿池价格获取接口
    print ("lend starting......................")
    URL= " http://123.56.166.152:10088/sunProject/tronbull?pool=TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu,TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA,TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK,TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i,TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ,TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs,TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj,TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz,TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs&tvl=98610.44,156609.16,388512.13,1399932.55,216661.72,2891855.65,185899.82,0.89,84.06"
    res = askrequests(url)
    lend_price_dict = getlpprice(res,"lend")
    lp_tvl_dict = {"TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu":108392.83,"TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA":156779.49,"TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK":39134.47,"TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i":1394056.91,"TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ":215752.37,"TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs":2879718.29,"TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj":185119.59,"TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz":0.89,"TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs":83.7}
    calculateApyDict = calApy(lp_tvl_dict,lend_price_dict,"lend")
    # lend_url= "http://123.56.166.152:10088/sunProject/tronbull?pool=TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu,TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA,TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK,TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i,TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ,TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs,TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj,TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz,TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs&tvl=94301.59,6529772.12,564058.59,1358969.88,205742.27,2795143.17,180875.3,0.8,78.96"
    lend_url = "http://123.56.166.152:10088/sunProject/tronbull?pool=TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu,TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA,TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK,TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i,TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ,TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs,TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj,TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz,TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs&tvl=108392.83,156779.49,39134.47,1394056.91,215752.37,2879718.29,185119.59,0.89,83.7"

    lend_apy_res = askrequests(lend_url)
    lend_apyDict = parse_apy(lend_apy_res,"lend")
    print ("计算：",calculateApyDict)
    print("接口：",lend_apyDict)
    judgment(calculateApyDict,lend_apyDict)
    print ("lend over......................")

if __name__ == '__main__':
    main()