import os,sys
import math
import requests
import json

#获取接口数据
def getUrl(address):
    url= "https://lendapi.just.network/justlend/yieldInfos?addr=%s&config=TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP$8400$14,TXJgMdjVX5dKiQaUi9QobwNxtSQaFqccvd$8400$14,TL5x9MtSnDy537FXKx53yAaHRRNdg9TkkA$2800$14,TGBr8uh9jBVHJhhkwSJvQN2ZAKzVkxDmno$2800$14,TRg6MnpsFXc82ymUPgf5qbj59ibxiEDWvv$2800$14,TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT$2800$14,TWQhCXaWz4eHK4Kd1ErSDHjMFPoPc9czts$2800$14,TUY54PVeH6WCcYCd6ZXXoBDsHytN9V5PXt$2800$14"%address
    # url ="https://lendapi.just.network/justlend/account?addr=%s"%address
    res = requests.get(url).text
    r = json.loads(res)
    print (r)
    return r
#计算sun apy 公式：
# (sun速度*365*1e18*sun价格/1e18)/((totalCash+totalBorrow-totalReserve) * 底池token价格 /1e18)
def sunApy(dict):
    res = getUrl("TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS")
    res_list  = res["data"]["assetList"]

    for e in res_list:
        if e["collateralSymbol"]=="SUN":
            price=float(e["assetPrice"])
    for ele in res_list:
        symble = ele["collateralSymbol"]
        print(symble+"=====starting=======")
        speed = dict[symble]
        totalcash = ele["totalCash"]
        totalborrow = ele["totalBorrow"]
        totalreserver = ele["totalReserve"]
        assetprice = float(ele["assetPrice"])
        tmp = float(totalcash) + float(totalborrow) - float(totalreserver)
        print(symble,speed,price,tmp,assetprice)
        formula = speed*365*1000000000000000000.0*price/1000000000000000000.0/\
                  tmp/assetprice*1000000000000000000.0
        print(formula)

# 计算公式
# trx数量=币数量(balance)*币精度(collateralDecimal)*币价格(assetPrice)/1e18/1e6
# TRX换成美元=TRX数量*TRX价格/1e18
def toUsd(dict):
    res = getUrl("TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS")
    res_list  = res["data"]["assetList"]
    price = float(res["data"]["trxPrice"])
    for ele in res_list:
        symble = ele["collateralSymbol"]
        if symble not in dict.keys():
            continue
        print(symble+"----------starting---------")
        assetprice = float(ele["assetPrice"])
        print(assetprice)
        if symble == "TRX":
            trxcount = dict[symble]
        else:
            colldec = ele["collateralDecimal"]
            dec = 1
            for i in range(colldec):
                dec *= 10
            trxcount = dict[symble]*dec*assetprice/1000000000000000000.0/1000000.0
        print (trxcount)
        to = trxcount * price/1000000000000000000.0
        print (to)

# 赚取收益=总持仓(页面显示的balance) - 总存款(account_supplyAdded/精度) + 总提现（account_redeemAdded/精度）
def earned(dict):
    res = getUrl("TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS")
    res_list  = res["data"]["assetList"]
    for ele in res_list:
        symble = ele.get("collateralSymbol","")
        print(symble+"----------starting---------")
        if symble not in dict.keys():
            continue
        else:
            colldec = ele["collateralDecimal"]
            dec = 1
            for i in range(colldec):
                dec *= 10
            supply = float(ele.get("account_supplyAdded",0))/dec
            redeem = float(ele.get("account_redeemAdded",0))/dec
            earn = dict[symble] - supply + redeem
            print (earn)

def main():
    #计算sun APY
    dict = {"TRX":600.0,"USDT":600.0,"USDJ":200.0,"SUN":200.0,"WIN":200.0,"BTC":200.0,"JST":200.0,"WBTT":200.0}
    sunApy(dict)
    # dict = {"TRX":2.5 ,"USDT":0.02}

    # toUsd(dict)
    # earned(dict)
if __name__=="__main__":
    main()