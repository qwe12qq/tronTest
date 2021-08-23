import os,sys
from utils import contractInteractive as contractTools

class checker():
    def __init__(self,fileName,duration):
        self.fileName = fileName
        self.contractInfo = {}
        self.duration = duration
        self.accountBase58 = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
        self.precision = {"TPDMF7GVzivR6heo3PzN85HZFLoGScd9Bb" : 1e6,"TKKMuQuMRrpcHYPoP55zmgkLwGgd1TMK2N": 1e6, \
                         "TBTK7orRXZxv9BLR7J22RDY2CY4Pv2Fkwm": 1e6,"TUp1BWfAZidkNbWkoiCjJcf4ctE4PAR2Rg": 1e18}
        self.contractObject = contractTools.contractObject("api.trongrid.io", self.accountBase58)

    def __resolveAddress(self,res):
        addressList = []
        tmpLit = []

        for i in range(0 , len(res) , 64):
            tmpLit.append(res[i : i+64])
        addressList.append(tmpLit[-1])
        if int(tmpLit[1],16) == 2:
            addressList.append(tmpLit[-2])
        return addressList

    def parseFile(self):
        with open(self.fileName) as f:
            lines = f.read().split("\n")

            for line in lines:
                if "type" in line or line == "":
                    continue
                line = line.split("\t")
                self.contractInfo[line[-1]] = {"name:" : line[0], "trx_speed" : line[1], "other_speed" : line[2]}
        # print (self.contractInfo)

    # methods: canNext()
    # returns: 0000000000000000000000000000000000000000000000000000000000000001 or 0000000000000000000000000000000000000000000000000000000000000000
    # methods:  DURATION_NEXT()
    # returns: 0000000000000000000000000000000000000000000000000000000000093a80
    def canDurationNext(self):

        for address,value in self.contractInfo.items():
            try:
                resDict = self.contractObject.triggerConstantContract(address, "canNext()")
                res = resDict.get("constant_result")[0]
                resInt = int(res,16)
                assert resInt == 1 , "警告：合约地址：%s, 本次续期不是自动续期模式，请手动检查参数，本次自动化验证流程不适用！！！" %(address)
                resDict = self.contractObject.triggerConstantContract(address,"DURATION_NEXT()")
                res = resDict.get("constant_result")[0]
                resInt = int(res,16)
                assert resInt == self.duration , "警告：合约地址：%s, 合约返回结果：%s, 续期周期不是7天，请手动确认DURATION_NEXT()参数！" % (address,resInt)
                print(address , "为自动续期模式，续期DURATION_NEXT check成功！")
            except Exception as e:
                print (e)
                return False
        return  True

    # methods: rewardNextData(address)
    # returns: 000000000000000000000000000000000000000000000000000008d4da62d880000000000000000000000000000000000000000000000000000008d4da62d880
    # methods: getRewardTokens()
    # returns: 0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a6337ae47a09aea0bbd4faeb23ca94349c7b774
    def rewards(self):

        for address,value in self.contractInfo.items():
            try:
                resDict = self.contractObject.triggerConstantContract(address, "getRewardTokens()")
                res = resDict.get("constant_result")[0]
                addlist = self.__resolveAddress(res)

                for ele in addlist:
                    print(address,ele)
                    resDict = self.contractObject.triggerConstantContract(address, "rewardNextData(address)",ele,"true")
                    res = resDict.get("constant_result")[0]
                    now,next = int(res[:64],16) , int(res[64:],16)

                    if 0 == int(ele,16):
                        trxspeed = float(self.contractInfo.get(address).get("trx_speed")) * 1e6
                        assert next - trxspeed == 0.0 , "警告：合约地址：%s, 合约查询数据：%s, 理论数据： %s, trx续期有问题，请手动检查！" % (address, next, trxspeed)
                    else:
                        othspeed = float(self.contractInfo.get(address).get("other_speed")) * self.precision.get(address)
                        assert next - othspeed == 0.0, "警告：合约地址：%s, 合约查询数据：%s, 理论数据： %s, 续期有问题，请手动检查！" % (address, next, trxspeed)
                print (address,"续期数据check成功！")
            except Exception as e :
                print(e)

def main():
    ch = checker("justswapSpeed",604800)
    ch.parseFile()
    assert ch.canDurationNext() == True," canDurationNext check failed!"
    ch.rewards()

if __name__ == '__main__':
    main()