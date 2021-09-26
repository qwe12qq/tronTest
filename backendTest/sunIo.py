import os,sys
import requests
import json
from utils import mysqlOperation as mysqlOperate
from utils import contractInteractive as contractOperate

class objenct():
    def __init__(self):
        self.accounts = ["TArXpybTZJG2819G9m3Np69ZJXFqz4UTfr","TE57xfg6d7qRZvsyyzd7x899JfKKyfcdoU","TFTosnoA2Th26qezdxmXMEsLrEerstzzHm","TKGRE6oiU3rEzasue4MsB6sCXXSTx9BAe3","TKZRPqoV7WLFvjhT4cEyBLv27Rvv1RNWGj","TLipJxwgDbn7FaQCnECxiYdxFTBhshLiW3","TLthCsi7GvwrrDVUws55sPiiTtMoMvmZ4Y","TPyVMgQ9gCpnP6oyHpKY2kEYPDCXm4KY7y","TS8v54PXszgnktpBm1JtzfXrDV7C4L8CwM","TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS","TVTji8akmVwaVd65NCWMAVfZtqrZjJbBu5"]
        self.sunIODict = {}
        self.op = ""
        self.mysqlinit()
        self.balanceDict = {}
        self.v2InfoDict = {}
        self.net = "api.nileex.io"
        self.account = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
        self.key = "127109F1B8FEC8CFAB6A3D4DCE13BBD748195BFD0B08F12FB2776446CC09A11F"
        self.initNet()
        self.tronObj = contractOperate.tronObject()
        self.rewardsDict = {}
        self.contract = {"TL6a2hVjNh3CZPcWWwbSXHxooWfuRaeYzu":"TPstc5LB5WHhhv8H5fQGfRMehDqHaPVkfG",
                    "TXEzEjv5iLmhrGGJfs1WqS9SVTW6myJP2H":"TRGdvFN6N7eXFH1dZHodi5intH25A9KNFH",
                    "TXKRytCcT471i6FNakDSHbTVsmKA7yqGH2":"THxRE7AFkZgPuptwm9bUEjuJm4cg7ax3ia"}


    def initNet(self):
        self.contractObj = contractOperate.contractObject(self.net, self.account,self.key)

    def mysqlinit(self):
        host = "123.56.166.152"
        port = 3306
        user = "defi"
        pw = "wEJdXe3LIsClKpk6"
        db = "defi-swapqa"
        self.op = mysqlOperate.mysqlOperate(host,port,user,pw,db)
        self.op.connect()

    def gegV2(self):
        url = "http://123.56.166.152:10088/ssp/getPoolDataV2"
        res = requests.get(url).text
        res = json.loads(res)
        data = res.get("data",{}).get("list",[])
        for ele in data:
            name = ele.get("name","")
            if name == "sspssp":
                self.v2InfoDict[name] = {"price":ele.get("price","")}
            elif name in ["THxRE7AFkZgPuptwm9bUEjuJm4cg7ax3ia","TPstc5LB5WHhhv8H5fQGfRMehDqHaPVkfG","TRGdvFN6N7eXFH1dZHodi5intH25A9KNFH"]:
                self.v2InfoDict[name]={"thisWeekApyV3":ele.get("thisWeekApyV3",""),"price":ele.get("price","")}
        # print(self.v2InfoDict)


    def sunIo(self):
        for ele in self.accounts:
            url = "http://123.56.166.152:10088/zapper/sunio/account?address=%s"%ele
            # print(url)
            res = requests.get(url).text
            res = json.loads(res)
            self.sunIODict[ele] = {}
            data = res.get("data",[])
            # print(res)
            for con in data[0]:
                key = list(con.get("balance",{}).keys())
                if len(key) == 0 :continue
                # print(key,len(key))
                self.sunIODict[ele][key[0]] = {"reward_value_in_usd":con.get("reward_value_in_usd",''),"balance":con["balance"][key[0]],
                                               "name":con.get("name",""),"stake_value_in_usd":con.get("stake_value_in_usd",""),
                                               "rewards":con["rewards"]["TDqjTkZ63yHB19w2n7vPm2qAkLHwn9fKKk"],
                                               "apy":con.get("apy","")}
        # print(self.sunIODict)

    def mysqlbalance(self):
        for ele in self.accounts:
            self.balanceDict[ele] = {}
            sql = 'select user_address,gauge_address,token_stake from ssp_gaugestake where user_address = "%s";'%ele
            l = self.op.selectMysql(sql)
            for con in l:
                if con[1] == "TL6a2hVjNh3CZPcWWwbSXHxooWfuRaeYzu":
                    self.balanceDict[ele]["TPstc5LB5WHhhv8H5fQGfRMehDqHaPVkfG"] = con[2]
                elif con[1] == "TXEzEjv5iLmhrGGJfs1WqS9SVTW6myJP2H":
                    self.balanceDict[ele]["TRGdvFN6N7eXFH1dZHodi5intH25A9KNFH"] = con[2]
                else:
                    self.balanceDict[ele]["THxRE7AFkZgPuptwm9bUEjuJm4cg7ax3ia"] = con[2]
        # print(self.balanceDict)

    def getrewards(self):

        for acc in self.accounts:
            self.rewardsDict[acc] = {}
            for ele in self.contract:
                accountHex = self.tronObj.base58ToHex(acc)
                parms = contractOperate.hexTo64Hex(str(accountHex)[2:])
                # print(parms)
                resDict = self.contractObj.triggerConstantContract(ele, "claimable_tokens_view(bytes32)",parms,"true")
                res = resDict.get("constant_result")[0]
                num = int(res,16)
                self.rewardsDict[acc][self.contract[ele]] = num
        # print(self.rewardsDict)

    def current(self,account,lpaddress):
        self.contract = {"TPstc5LB5WHhhv8H5fQGfRMehDqHaPVkfG":"TL6a2hVjNh3CZPcWWwbSXHxooWfuRaeYzu",
                         "TRGdvFN6N7eXFH1dZHodi5intH25A9KNFH":"TXEzEjv5iLmhrGGJfs1WqS9SVTW6myJP2H",
                         "THxRE7AFkZgPuptwm9bUEjuJm4cg7ax3ia":"TXKRytCcT471i6FNakDSHbTVsmKA7yqGH2"}
        lpaddressHex = self.tronObj.base58ToHex(self.contract[lpaddress])
        parms = contractOperate.hexTo64Hex(str(lpaddressHex)[2:])
        accountHex = self.tronObj.base58ToHex(account)
        parms += contractOperate.hexTo64Hex(str(accountHex)[2:])
        Hex = self.tronObj.base58ToHex("TGrf5rSstQTkA3HysqFFUBqX5Ffn1FqzA3")
        parms += contractOperate.hexTo64Hex(str(Hex)[2:])
        resDict = self.contractObj.triggerConstantContract("TBNwPKrvcoSffbRUTtDETjT2CBDSJweE94", "_current(address,address,address)",parms,"true")
        res = resDict.get("constant_result")[0]
        cur = int(res[:64],16)
        # print (float(cur)/1e18,self.contract[lpaddress])
        return float(cur)/1e18


    def parseRes(self):
        sspprice = float(self.v2InfoDict.get("sspssp",{}).get("price",0))
        for account,info in self.sunIODict.items():

            for key,value in info.items():
                # print(account,key,value)
                num = self.current(account,key)
                # print(self.v2InfoDict,"000------")
                apyV3 = float(self.v2InfoDict.get(key,{}).get("thisWeekApyV3",0))
                print(apyV3*num*100/2.5,value.get("apy",0))
                assert float(apyV3*num*100/2.5)- float(value.get("apy",0)) <0.1



                balance = value.get("balance",0)
                assert self.balanceDict[account][key] == balance,"balance failed!"
                price = float(self.v2InfoDict.get(key,{}).get("price",0))
                if "TRGdvFN6N7eXFH1dZHodi5intH25A9KNFH" == key:
                    assert float(value.get("stake_value_in_usd",0))-float(value.get("balance",0))/1e6*price<0.00001,"stake_value_in_usd failed!"
                else:
                    assert float(value.get("stake_value_in_usd",0))-float(value.get("balance",0))/1e18*price<0.00001,"stake_value_in_usd failed!"
                assert float(value.get("reward_value_in_usd",0)) - float(value.get("rewards",0))/1e18*sspprice < 0.0001,"rewards failed!"
                print(float(value.get("rewards",0))/1e18 ,float(self.rewardsDict[account][key])/1e18)
                assert float(value.get("rewards",0))/1e18 - float(self.rewardsDict[account][key])/1e18 < 0.0001

def main():

    ob = objenct()
    ob.gegV2()
    ob.getrewards()
    ob.sunIo()
    ob.mysqlbalance()
    ob.parseRes()

if __name__ == '__main__':
    main()