import os,sys
import random
import time,datetime
from time import sleep
import utils.contractInteractive as contractOperate

class gaugeObject():
    def __init__(self,net,gauge_address,vote,VotingEscrow):
        self.accountNow = ""
        self.gaugeAddressList = gauge_address
        self.vote = gauge_address
        self.net = net
        self.voteEscrow = VotingEscrow
        self.accountBase58 = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
        self.tronObj = contractOperate.tronObject()
        self.key = ""

    def init(self,account,key):
        self.accountNow = account
        self.key = key
        self.accountHex = self.tronObj.base58ToHex(self.accountNow)
        self.contractObj = contractOperate.contractObject(self.net, self.accountNow,self.key)

    def gaugeDeposit(self):
        randInt = random.randint(1,30) * 100000000000000000
        h = hex(randInt)
        parms = contractOperate.hexTo64Hex(str(h)[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.gaugeAddressList[0],"deposit(uint256)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            # print (txid,res.get("receipt",{}).get("result",""))
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger deposit() failed!"
            print("Deposit amount:",randInt)
            return randInt
        except Exception as e:
            print(e)
            return -1

    def gaugeWithdraw(self):
        randInt = random.randint(1,10) * 10000000000
        h = hex(randInt)
        parms = contractOperate.hexTo64Hex(str(h)[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.gaugeAddressList[0],"withdraw(uint256)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            # print (res.get("receipt",{}).get("result",""))
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger withdraw() failed!"
            print("withdraw amount:",randInt)
            return randInt
        except Exception as e:
            print(e)
            return -1

    def gaugeBalanceAddr(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "balanceOf(address)",account,"true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def gaugeTotalSupply(self):
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "totalSupply()","","true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def gaugeWorkingBalances(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "working_balances(address)",account,"true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def gaugeWorkingSupply(self):
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "working_supply()","","true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def voteEscBalanceOf(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        resDict = self.contractObj.triggerConstantContract(self.voteEscrow, "balanceOf(bytes32)",account,"true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def voteEscTotalSupply(self):
        resDict = self.contractObj.triggerConstantContract(self.voteEscrow, "totalSupply()","","true")
        res = resDict.get("constant_result")[0]
        # print(int(res,16))
        return int(res,16)

    def inflationRate(self):
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "inflation_rate()","","true")
        res = resDict.get("constant_result")[0]
        print(int(res,16))
        return int(res,16)

    def integrateFraction(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        resDict = self.contractObj.triggerConstantContract(self.gaugeAddressList[0], "integrate_fraction(address)",account,"true")
        res = resDict.get("constant_result")[0]
        print(int(res,16))
        return int(res,16)

    def userCheckpoint(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.gaugeAddressList[0],"user_checkpoint(address)",account,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            # print (res.get("receipt",{}).get("result",""))
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger withdraw() failed!"
        except Exception as e:
            print(e)

    def claimTokens(self):
        account = contractOperate.hexTo64Hex(self.accountHex[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.gaugeAddressList[0],"claimable_tokens(address)",account,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            # print(res)
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger withdraw() failed!"
            # print(int(res.get("contractResult",['0'])[0],16))
            return int(res.get("contractResult",['0'])[0],16),res.get("blockTimeStamp",0)
        except Exception as e:
            print(e)
            return -1

    # calcBoost(address _vesun, address _pool, address _user)
    def voteBalanceTotal(self):
        param = "000000000000000000000000f256c0df4a66c53f15ae724e90b1b39f41318d8b"+ \
                "000000000000000000000000a32bc4c8d7d1124af87766b4152bcfd4842a2405"+ \
                "000000000000000000000000be16fd25b87f12bbec7ba29028f05471000582a7"
        resDict = self.contractObj.triggerConstantContract("TQ8nqwcP2XoaukAf4AyGHMyPEXFCqqTSkr", "calcBoost(address,address,address)",param,"true")
        res = resDict.get("constant_result")[0]
        votebalance,votetotal = res[128:192],res[192:256]
        # print(int(votebalance,16),int(votetotal,16))
        return int(votebalance,16),int(votetotal,16)

    def increaseVesun(self):
        randInt = random.randint(1,10) * 1000000000000000000
        h = hex(randInt)
        h2 = contractOperate.hexTo64Hex(str(h)[2:])
        parms = h2+contractOperate.hexTo64Hex(str("0"))
        try:
            txid = self.contractObj.TriggerSmartContract("TNbSWYamJayfhe89pURBBVG2hUzd68mzdT","increaseLock(uint256,uint256)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            # print (res.get("receipt",{}).get("result",""))
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger increaseLock() failed!"
            print("increaseLock amount:",randInt)
        except Exception as e:
            print(e)

    def getResource(self):
        gaugeBalanceBefore = self.gaugeBalanceAddr()
        gaugeTotalSupplyBefore = self.gaugeTotalSupply()
        gaugeWorkingBalancesBefore = self.gaugeWorkingBalances()
        gaugeWorkingSupplyBefore = self.gaugeWorkingSupply()
        return gaugeBalanceBefore,gaugeTotalSupplyBefore,gaugeWorkingBalancesBefore,gaugeWorkingSupplyBefore

    def testClaimableWorker(self,startTime,weight,endTime):
        rate = self.inflationRate()
        startTime = int(time.mktime(time.strptime(startTime,'%Y-%m-%d %H:%M:%S')))
        amount,endtime = self.claimTokens()
        endtime = int(time.mktime(time.strptime(endTime,'%Y-%m-%d %H:%M:%S')))
        times = int(endtime) - startTime
        print(startTime,amount,endtime,times)
        workingBalance = self.gaugeWorkingBalances()
        workingSupply = self.gaugeWorkingSupply()
        print(workingBalance,workingSupply)
        amountThory = int(rate * weight/1e18 * times * workingBalance/workingSupply)
        print(amountThory)
        assert amount - amountThory == 0





    def testBalanceWorking(self):
        print(self.accountNow,self.key)
        self.increaseVesun()
        gaugeBalanceBefore,gaugeTotalSupplyBefore,gaugeWorkingBalancesBefore,gaugeWorkingSupplyBefore = self.getResource()
        voteEscBalanceOf,voteEscTotalSupply = self.voteBalanceTotal()
        print("vote: ",voteEscBalanceOf,voteEscTotalSupply)

        depositAmount = self.gaugeDeposit()
        gaugeBalanceAfter,gaugeTotalSupplyAfter,gaugeWorkingBalancesAfter,gaugeWorkingSupplyAfter = self.getResource()
        print("Before:",gaugeBalanceBefore,gaugeTotalSupplyBefore,gaugeWorkingBalancesBefore,gaugeWorkingSupplyBefore)
        print("After:",gaugeBalanceAfter,gaugeTotalSupplyAfter,gaugeWorkingBalancesAfter,gaugeWorkingSupplyAfter)
        assert gaugeBalanceAfter - gaugeBalanceBefore == depositAmount,"After deposit,BalanceAfter:%s BalanceBefore:%s failed!"%(gaugeBalanceAfter,gaugeBalanceBefore)
        assert gaugeTotalSupplyAfter - gaugeTotalSupplyBefore == depositAmount,"After deposit,BalanceAfter:%s BalanceBefore:%s failed!"%(gaugeTotalSupplyAfter,gaugeTotalSupplyBefore)
        tmp = gaugeBalanceAfter * 0.4 + gaugeTotalSupplyAfter * voteEscBalanceOf/voteEscTotalSupply * (100-40)/100
        addWorking = min(gaugeBalanceAfter,tmp)
        print("addWorking:",int(addWorking)," voteEscBalanceOf/voteEscTotalSupply:",voteEscBalanceOf/voteEscTotalSupply)
        print("Gap:",gaugeWorkingBalancesAfter-int(addWorking))
        assert abs(gaugeWorkingBalancesAfter-int(addWorking)) < 1e9,"After deposit,workingBalanceAfter:%s addWorking:%s failed!"%(gaugeWorkingBalancesAfter,addWorking)
        assert gaugeWorkingSupplyAfter - gaugeWorkingSupplyBefore == gaugeWorkingBalancesAfter - gaugeWorkingBalancesBefore, \
            "After deposit,gaugeWorkingSupplyAfter:%s gaugeWorkingSupplyBefore:%s failed!"%(gaugeWorkingSupplyAfter,gaugeWorkingSupplyBefore)

        voteEscBalanceOf,voteEscTotalSupply = self.voteBalanceTotal()
        print("vote2: ",voteEscBalanceOf,voteEscTotalSupply)
        withdrwAmount = self.gaugeWithdraw()
        gaugeBalanceAfter2,gaugeTotalSupplyAfter2,gaugeWorkingBalancesAfter2,gaugeWorkingSupplyAfter2 = self.getResource()
        print("after2:",gaugeBalanceAfter2,gaugeTotalSupplyAfter2,gaugeWorkingBalancesAfter2,gaugeWorkingSupplyAfter2)
        tmp = gaugeBalanceAfter2 * 0.4 + gaugeTotalSupplyAfter2 * voteEscBalanceOf/voteEscTotalSupply * (100-40)/100
        withdrawWorking = min(gaugeBalanceAfter2,tmp)
        print("withdrawWorking:",int(withdrawWorking)," voteEscBalanceOf/voteEscTotalSupply:",voteEscBalanceOf/voteEscTotalSupply)
        print("Gap:",gaugeWorkingBalancesAfter2-int(withdrawWorking))
        assert gaugeBalanceAfter - gaugeBalanceAfter2 == withdrwAmount,"After withdraw,BalanceAfter2:%s,BalanceAfter:%s failed!"%(gaugeBalanceAfter2,gaugeBalanceAfter)
        assert gaugeTotalSupplyAfter - gaugeTotalSupplyAfter2 == withdrwAmount,"After withdraw,TotalSupplyAfter2:%s,TotalSupplyAfter:%s failed!"%(gaugeTotalSupplyAfter2,gaugeTotalSupplyAfter)
        assert abs(gaugeWorkingBalancesAfter2-int(withdrawWorking)) < 1e9,"After withdraw,workingBalanceAfter2:%s withdrawWorking:%s failed!"%(gaugeWorkingBalancesAfter2,withdrwAmount)
        assert gaugeWorkingSupplyAfter - gaugeWorkingSupplyAfter2 == gaugeWorkingBalancesAfter - gaugeWorkingBalancesAfter2, \
            "After withdraw,gaugeWorkingSupplyAfter2:%s gaugeWorkingSupplyAfter:%s failed!"%(gaugeWorkingSupplyAfter2,gaugeWorkingSupplyAfter)

def main():
    accounts = {"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS":"127109F1B8FEC8CFAB6A3D4DCE13BBD748195BFD0B08F12FB2776446CC09A11F",
                "TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq":"BB3D61EF9A49E425BC01C2B8ACB4C4647092CEBD6C2F2A815804520FBAA60E60"}
    gauge_address = ["TUiJq39Ny3CM6uR25pLQSkeCgrcKDrz69u","TCHCGGZF5cw64niNARCxUTCDG6oc4aykF4","TV8qyJcJ6c9GRkJAKXLfNdh5w3nq6KPF76"]
    vote = "TJch67UEStiM6GooDPrZBY9kuYr4mXXgdb"
    VotingEscrow = "TY4aTDPNNrTWdPd6nGbqjWCaAshYSGYaoq"
    net = "api.nileex.io"
    ob = gaugeObject(net,gauge_address,vote,VotingEscrow)
    ob.init("TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq",accounts["TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq"])
    ob.testClaimableWorker("2021-09-07 12:00:00",1e18,"2021-09-07 14:00:00")



    # for i in range(100):
    #     print(i," start--------------------")
    #     ob.init("TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS",accounts["TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"])
    #     print("account TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS.................")
    #     ob.testWorking()
    #     ob.init("TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq",accounts["TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq"])
    #     print("account TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq.................")
    #     ob.testWorking()
    #     print(i," end---------------------")


if __name__ =="__main__":
    main()