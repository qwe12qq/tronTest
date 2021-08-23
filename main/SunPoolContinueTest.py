import os,sys
import time,datetime
from utils import contractInteractive as contractTools

class SunPoolCheck:
    def __init__(self,endTime):
        self.endTime = endTime
        self.poolAddressRewards = {}
        self.poolPrecisionDict = {'SUN-TRX-LP':1e18,'JST-TRX-LP':1e18,'USDT-TRX-LP':1e18,\
                                  'USDJ-TRX-LP':1e18,'BTC-TRX-LP':1e18, 'WBTT-TRX-LP':1e18,\
                                  'WIN-TRX-LP':1e18,'ETH-TRX-LP':1e18,'TUSD-TRX-LP':1e18,\
                                  'NFT-TRX-LP':1e18,'YFX-TRX-LP':1e18
                                  }

    def __calcuRewards(self,reward,name):
        res = 0
        res = int(reward,16) * 3600 * 24 * 7 /self.poolPrecisionDict.get(name)
        return res

    def __calcuPeriod(self,period):
        flag = False
        timeArray = time.strptime(self.endTime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        print(period,timeStamp)
        if abs(period-timeStamp) < 30:
            flag = True
        return flag

    def parseRewards(self):
            with open("../data/sunPoolRewards",'r') as f:
                fl = f.readlines()
                for line in fl:
                    if line=="\n" :continue
                    line = line.replace("\n",'').split("\t")
                    pool,add,rew = line[0],line[1],int(line[2]) * 7
                    self.poolAddressRewards[pool] = {"address": add ,"reward": rew}

    def checkParams(self):
        account = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
        for pool,items in self.poolAddressRewards.items():
            try:
                address,rewardTheory = items["address"],items["reward"]
                addressCode = contractTools.getAccountToABIFormat(address)
                resDict = contractTools.triggerConstantContract(address, "rewardRate()", account)
                rewardActual = self.__calcuRewards(resDict["constant_result"][0],pool)
                print(pool ,float(rewardTheory),float(rewardActual))
                assert abs(rewardTheory - rewardActual) < 1e-1, \
                    "%s rewardTheory:%s rewardActual:%s is greater than the threshold ！！" \
                    % (pool,rewardTheory,rewardActual)
            except Exception as e:
                print (e)
            try:
                resDict = contractTools.triggerConstantContract(address, "DURATION()", account)
                during = "0000000000000000000000000000000000000000000000000000000000093a80"
                resDuring = resDict["constant_result"][0]
                assert resDuring == during,"%s DURATION is not equal!resDuring: %s" %(pool,resDuring)
            except Exception as e:
                print (e)
            try:
                resDict = contractTools.triggerConstantContract(address, "periodFinish()", account)
                resFinish = int(resDict["constant_result"][0],16)
                f = self.__calcuPeriod(resFinish)
                assert f is True,"%s periodFinish() period :%s is error！" % (pool, resFinish)
            except Exception as e:
                print (e)
            try:
                if pool == "TUSD-TRX-LP":
                    resDict = contractTools.triggerConstantContract(address, "rewardNow()", account)
                    rewardNow = int(resDict["constant_result"][0],16)/self.poolPrecisionDict.get(pool)
                    print(pool,int(rewardTheory),int(rewardNow))
                    assert int(rewardTheory) - int(rewardNow) < 0.1,"%s rewardNow() rewardTheory:%s rewardNow:%s" \
                    %(pool, rewardTheory,rewardNow)
            except Exception as e:
                print (e)

def main():
    p = SunPoolCheck("2021-6-07 21:00:00")
    p.parseRewards()
    p.checkParams()

if __name__ == '__main__':
    main()