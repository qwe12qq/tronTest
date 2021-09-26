import os,sys
import requests
from utils import contractInteractive as contractOperate

class staker:
    def __init__(self,account,key,stakeManagerProxy):
        self.net = "api.nileex.io"
        self.account = account
        self.key = key
        self.stakeManagerProxy = stakeManagerProxy
        self.tronObj = contractOperate.tronObject()
        self.accountHex = self.tronObj.base58ToHex(self.account)

    def initNet(self):
        self.contractObj = contractOperate.contractObject(self.net, self.account,self.key)

    def stakeFor(self,user,amount,hemalfee,acceptFlag,pubkey):
        print("stakefor:")
        userHex = self.tronObj.base58ToHex(user)
        parms = contractOperate.hexTo64Hex(str(userHex)[2:])
        amounthex = hex(amount)
        parms += contractOperate.hexTo64Hex(str(amounthex)[2:])
        hemfeehex = hex(hemalfee)
        parms += contractOperate.hexTo64Hex(str(hemfeehex)[2:])
        acceptFlagHex = hex(acceptFlag)
        parms += contractOperate.hexTo64Hex(str(acceptFlagHex)[2:])
        parms += "00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000040"
        parms += pubkey
        try:
            txid = self.contractObj.TriggerSmartContract(self.stakeManagerProxy,"stakeFor(address,uint256,uint256,bool,bytes)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger stakeFor failed!"
        except Exception as e:
            print(e)

    def unstake(self,num):
        h = hex(num)
        parms = contractOperate.hexTo64Hex(str(h)[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.stakeManagerProxy,"unstake(uint256)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            print(res)
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger unstake failed!"
        except Exception as e:
            print(e)

    def unstakeClaim(self,num):
        h = hex(num)
        parms = contractOperate.hexTo64Hex(str(h)[2:])
        try:
            txid = self.contractObj.TriggerSmartContract(self.stakeManagerProxy,"unstakeClaim(uint256)",parms,0)
            res = self.contractObj.gettransactioninfobyid(txid)
            print(res)
            assert res.get("receipt",{}).get("result","") == "SUCCESS","trigger unstakeClaim failed!"
        except Exception as e:
            print(e)

    def currentValidatorSetSize(self):
        resDict = self.contractObj.triggerConstantContract(self.stakeManagerProxy, "currentValidatorSetSize()","","true")
        res = resDict.get("constant_result")[0]
        print(int(res,16))
        # return int(res,16)

    def validators(self,num=1):
        h = hex(num)
        parms = contractOperate.hexTo64Hex(str(h)[2:])
        resDict = self.contractObj.triggerConstantContract(self.stakeManagerProxy, "validators(uint256)",parms,"true")
        res = resDict.get("constant_result")[0]
        amount64,singer64,contratAddress64 = res[:64],res[320:384],res[384:448]
        amount = int(amount64,16)
        print(amount,singer64,contratAddress64)
        return amount,singer64,contratAddress64

def main():
    account = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
    key = "127109F1B8FEC8CFAB6A3D4DCE13BBD748195BFD0B08F12FB2776446CC09A11F"
    # account = "TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq"
    # key = "BB3D61EF9A49E425BC01C2B8ACB4C4647092CEBD6C2F2A815804520FBAA60E60"

    stakeManagerProxy = "TCV5znJpqdvxRmaeL7RfL7E1JVzdmm3xy5"
    st = staker(account,key,stakeManagerProxy)
    st.initNet()
    st.currentValidatorSetSize()
    st.validators(6)
    amount = 1000000000000000000
    # st.stakeFor(account,amount,1000000000000000000,1,
    #             '657BB3074961EBA25673840D9CD8DDECAB487CD0C09908350658232F91F152C8B2A0D401FD1CC85BCB823B1CFAC7C8E4A68AFE95FF914094A5C625A30C97DEC7')
    # st.currentValidatorSetSize()
    # st.unstake(6)
    st.unstakeClaim(4)
    st.currentValidatorSetSize()

if __name__=="__main__":
    main()
