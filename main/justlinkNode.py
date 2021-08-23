import os,sys

import json,requests
import datetime,time
import random
sys.path.append("/Users/lanyu/liuyl/coding/code_factory/web_test/demo");
from utils import contractInteractive as contractTools

class testJustlink:
    def __init__(self,net):
        self.accountBase58 = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
        self.toolsObject = contractTools.contractObject(net, self.accountBase58)
        self.contractAddress = "TGK1jmj8fk93STx8KR1YG3FrQ4cqagAJow"
        self.randomList = []

    def triggerVRFCoordinator(self):
        contractaddress = "TRAzWb5GEeisTzpDENju2Bg7Yh31ia5ZDU"
        res = self.toolsObject.triggerConstantContract(contractaddress,"withdrawableTokens(address)","000000000000000000000000fa13014b0891d8474444561e709061d83b5b75fa")
        assert res.get("result").get("result") == True,"Trigger withdrawableTokens failed!"
        r = int(res.get("constant_result")[0],16)
        print (r)
        return r

    def manger(self):
        count = 0
        before = self.triggerVRFCoordinator()
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for i in range(200):
            print ("Start execution for the %s time........................."%i)
            resuestid = self.triggerRollDice()
            if resuestid == "": continue
            count += 1
            time.sleep(13)
            if self.listenEvent(resuestid) == False:
                print("listenEvent has not result!!try again.....")
                time.sleep(5)
                if self.listenEvent(resuestid) == False:
                    print ("listenEvent failed! Please check.....")
                    print (count)
                    self.checkRes()
                    continue
            print ("End of execution %s times........................."%i)
        print ("count: ",count)
        self.checkRes()
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        after = self.triggerVRFCoordinator()
        # assert after-before == 1000*count,"withdrawableTokens failed! before:%s,after:%s"%(before,after)

    def triggerRollDice(self):
        d64 = contractTools.hexTo64Hex(str(random.randint(1,50)))
        add = contractTools.hexTo64Hex("fa13014b0891d8474444561e709061d83b5b75fa")
        prms = d64 + add
        requestid = ""
        try:
            txid = self.toolsObject.TriggerSmartContract(self.contractAddress,"rollDice(uint256,address)",prms,0)
            res = self.toolsObject.gettransactioninfobyid(txid)
            print (res.get("receipt",{}).get("result",""))
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger RollDice() failed!"
            requestid = res.get("contractResult")[0]
            print ("triggerRollDice requestid: ",requestid)
        except Exception as e:
            print(e)
        return requestid

    def listenEvent(self,resuestId):
        url = "https://nileapi.tronscan.org/api/contracts/smart-contract-triggers-batch?fields=hash,method"
        body = {"contractAddress":"TGK1jmj8fk93STx8KR1YG3FrQ4cqagAJow"}
        headers = {"Accept": "application/json","Content-Type": "application/json"}
        res = requests.post(url, json.dumps(body), headers = headers)
        assert res.ok == True ,"listen event is failed!"
        res = json.loads(res.text)
        flag = False
        for ele in res["event_list"]:
            if resuestId != ele.get("result",{}).get("requestId","") or ele.get("event_name","") != "DiceLanded":
                continue
            else:
                result = ele.get("result",{}).get("result")
                print ("result: ",result)
                self.randomList.append(result)
                flag = True
        return flag

        # DiceLandedcontent = res["event_list"][0]
        # if DiceLandedcontent.get("event_name","") != "DiceLanded":
        #     print ("DiceLanded is not new!!")
        #     return False
        # if resuestId != DiceLandedcontent.get("result",{}).get("requestId",""):
        #     print ("DiceLanded resuestId is not equal!!")
        #     return False
        # # print ("DiceLandedcontent: ",DiceLandedcontent)
        # result = DiceLandedcontent.get("result",{}).get("result")
        # print ("result: ",result)
        # self.randomList.append(result)
        # return True

    def checkRes(self):
        # self.randomList = [1,2,3,4,5,5,4,2,1]
        self.randomList.sort()
        print ("randomList: ",self.randomList)
        print("randomList length: ",len(self.randomList))
        # assert len(list(set(self.randomList))) == len(self.randomList),"randomList has duplicate elements!!!"

        for i in self.randomList:
            if self.randomList.count(i) > 1:
                print("元素{},重复{}次".format(i, self.randomList.count(i)))

def main():
    net = "api.nileex.io"
    jk = testJustlink(net)
    jk.manger()

if __name__ == '__main__':
    main()