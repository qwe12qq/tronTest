import os,sys
import json
import requests
from time import sleep
from tronapi import Tron,HttpProvider

class tronObject():
    def __init__(self):
        self.full_node = HttpProvider('https://api.nileex.io')
        self.solidity_node = HttpProvider('https://api.nileex.io')
        self.event_server = HttpProvider('https://api.nileex.io')
        self.tron = Tron(full_node=self.full_node,solidity_node=self.solidity_node,event_server=self.event_server)

    def base58ToHex(self,base58):
        hex = self.tron.address.to_hex(base58)
        return hex

    def hexToBase58(self,hex):
        base58 = self.tron.address.from_hex(hex)
        return base58

    def gettransaction(self,txId):
        result = self.tron.trx.get_transaction(txId)
        return result

    def gettransactioninfobyid(self,txId):
        result = self.tron.trx.get_transaction_info(txId)
        return result


class contractObject():
    def __init__(self,httpNode,account,key = "127109F1B8FEC8CFAB6A3D4DCE13BBD748195BFD0B08F12FB2776446CC09A11F"):
        self.httpNode = httpNode  # api.trongrid.io or api.nileex.io
        self.account = account
        self.key = key
        self.headers = {"Accept": "application/json","Content-Type": "application/json"}

    # URL： https://api.trongrid.io/wallet/triggerconstantcontract
    # body： {"contract_address":"TDqjTkZ63yHB19w2n7vPm2qAkLHwn9fKKk","function_selector":"decimals()","parameter":"","fee_limit":10,"call_value":0,"owner_address":"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"}'
    # visibleFlag:true  TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS   visibleFlag:false 416a6337ae47a09aea0bbd4faeb23ca94349c7b774
    def triggerConstantContract(self,contractAddress,methodName, param="" , visibleFlag = "true"):
        url = "https://{}/wallet/triggerconstantcontract" .format(self.httpNode)
        body = '{"contract_address":"%s","function_selector":"%s","parameter":"%s","fee_limit":100,"call_value":0,"owner_address":"%s","visible": %s}'\
               %(contractAddress, methodName, param, self.account, visibleFlag)
        # print(url,body)
        response = json.loads(requests.post(url, body, headers = self.headers).text)

        if response["result"]["result"] == True:
            return response
        else:
            return {}


    # https://api.trongrid.io/v1/accounts/TUvT7ZRK8ijh9BUVL4gvfRZ3UjzoVHvkiW
    def getAccountToABIFormat(self, base58Account):
        accountCode = ""
        url = "https://{}/v1/accounts/{}".format(self.httpNode, base58Account)
        response = json.loads(requests.get(url, headers = self.headers).text)

        if response["success"] == True:
            accountCode = response.get("data")[0].get("address")
        return accountCode

    def getAccount(self,account,visible = "true"):
        url = "https://{}/wallet/getaccount".format(self.httpNode)
        body = {"address": account, "visible": visible}
        response = requests.post(url, json.dumps(body), headers = self.headers).text
        return response

    # URL： http://47.252.3.238:8090/wallet/getcontract
    # body: {"value":"TNtrTKmkKWoYYucELGjDRsAAqQcwwWHyAz","visible": True}
    def getContract(self,contractAddress,visible = "true"):
        url = "https://{}/wallet/getcontract".format(self.httpNode)
        body = {"value": contractAddress,"visible": visible}
        response = json.loads(requests.post(url, json.dumps(body), headers = self.headers).text)
        return response

    # url  https://api.nileex.io/wallet/triggersmartcontract
    # body: {"contract_address":"TDPEv6sZj49KzR2jjdTZ7EQMFB3DPDoyWf","owner_address":"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS",
    # "function_selector":"add_liquidity(uint256[3],uint256)","parameter":"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640000000000000000000000000000000000000000000000000000000000000000",
    # "call_value":0,"visible":True,"fee_limit":300000000}
    def TriggerSmartContract(self,contractAddress,functionName,params,callvalue,visible = "true"):
        url = "https://{}/wallet/triggersmartcontract". format(self.httpNode)
        body = '{"contract_address":"%s","owner_address":"%s","function_selector":"%s","parameter":"%s",' \
               '"fee_limit":5000000000, "call_value":%s,"visible": %s}'% \
               (contractAddress, self.account, functionName, params, callvalue, visible)
        # print(url,body)
        response = requests.post(url, body, headers = self.headers).text
        responseSign = self.gettransactionsign(response)
        responseBroad = self.broadcastTransaction(responseSign)
        sleep(3)
        assert json.loads(responseBroad).get("result") == True,"Trigger SmartContract failed!"
        txid = json.loads(responseBroad).get("txid")
        return txid


    # url: https://api.nileex.io/wallet/gettransactioninfobyid
    # body: {"value":"bbcc104f39d919f21c16b0de8f32ed6355449b36b5369d17f612d8337b99741f","visible":false}
    def gettransactioninfobyid(self,txid):
        url = "https://{}/wallet/gettransactioninfobyid". format(self.httpNode)
        body = {"value":txid}
        response = requests.post(url, json.dumps(body), headers = self.headers).text
        res = json.loads(response)
        # print ("gettransactioninfobyid: " + response)
        assert res.get("receipt",{}).get("result") == "SUCCESS","txid:%s , gettransactioninfobyid is failed!" % txid
        return res

    # url: https://api.nileex.io/wallet/deploycontract
    # body: {"owner_address": "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS","abi": "[{\"constant\":false,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"},{\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"set\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"}],\"name\":\"get\",\"outputs\":[{\"name\":\"value\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]",
    # "bytecode": "608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029",
    # "fee_limit": 1000000,"origin_energy_limit": 100000,"name": "SomeContract","call_value": 0,"visible": True,"consume_user_resource_percent": 100}
    def deployContract(self,abi,bytecode,params,originEnergyLimit,name,callValue,consumeUserResourcePercent):
        url = "https://{}/wallet/deploycontract". format(self.httpNode)
        body = {"owner_address": self.account,"abi": abi, "bytecode": bytecode, "parameter": params,
                "fee_limit":5000000000,"origin_energy_limit": originEnergyLimit,"name": name,"call_value":callValue,
                "consume_user_resource_percent": consumeUserResourcePercent }
        responseDeploy = requests.post(url, json.dumps(body), headers = self.headers).text
        # print("deploy: ",responseDeploy)
        responseSign = self.gettransactionsign(responseDeploy)
        responseBroad = self.broadcastTransaction(responseSign)
        sleep(3)
        assert json.loads(responseBroad).get("result") == True,"deploy contract failed!"
        txid = json.loads(responseBroad).get("txid")
        res = self.gettransactioninfobyid(txid)
        contractAddress = res.get("contract_address","")
        return contractAddress

    # sign: URL：https://api.nileex.io/wallet/gettransactionsign
    # body: {"transaction":"{\"visible\":false,\"txID\":\"17d6e58c0c8c474ed6597ea3331adbb2cb7762844cf0ffd88d6a059f43d41c05\",\"contract_address\":\"412a328f345b9c4f24c38221d7e787071c6b0e7243\",\"raw_data\":{\"contract\":[{\"parameter\":{\"value\":{\"owner_address\":\"41104669fa7a3dea599c0fbd823f0911565721ed7b\",\"new_contract\":{\"bytecode\":\"608060405234801561001057600080fd5b50d3801561001d57600080fd5b50d2801561002a57600080fd5b5060af806100396000396000f3fe60806040526004361060305760003560e01c80631b27274b1460355780633a7852381460715780634dec9b57146035575b600080fd5b348015604057600080fd5b50d38015604c57600080fd5b50d28015605857600080fd5b50605f6074565b60408051918252519081900360200190f35b605f5b60019056fea2646970667358221220188c1499dd33ba3a8221883471a78a67be5d60f1bc41e01ae8729ed43c4d9fc964736f6c63430007000033\",\"consume_user_resource_percent\":100,\"name\":\"testConstantContract\",\"origin_address\":\"41104669fa7a3dea599c0fbd823f0911565721ed7b\",\"abi\":{\"entrys\":[{\"outputs\":[{\"name\":\"z\",\"type\":\"uint256\"}],\"name\":\"testPayable\",\"stateMutability\":\"Payable\",\"type\":\"Function\"},{\"outputs\":[{\"name\":\"z\",\"type\":\"uint256\"}],\"name\":\"testPure\",\"stateMutability\":\"Pure\",\"type\":\"Function\"},{\"outputs\":[{\"name\":\"z\",\"type\":\"uint256\"}],\"name\":\"testView\",\"stateMutability\":\"View\",\"type\":\"Function\"}]},\"origin_energy_limit\":11111111111111}},\"type_url\":\"type.googleapis.com/protocol.CreateSmartContract\"},\"type\":\"CreateSmartContract\"}],\"ref_block_bytes\":\"bcef\",\"ref_block_hash\":\"4c7ee8a640869500\",\"expiration\":1624348047000,\"fee_limit\":1000000000,\"timestamp\":1624347988911},\"raw_data_hex\":\"0a02bcef22084c7ee8a6408695004098edc095a32f5ad503081e12d0030a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e7472616374129b030a1541104669fa7a3dea599c0fbd823f0911565721ed7b1281030a1541104669fa7a3dea599c0fbd823f0911565721ed7b1a5d0a1f1a0b7465737450617961626c652a0c12017a1a0775696e74323536300240040a1c1a0874657374507572652a0c12017a1a0775696e74323536300240010a1c1a0874657374566965772a0c12017a1a0775696e743235363002400222e801608060405234801561001057600080fd5b50d3801561001d57600080fd5b50d2801561002a57600080fd5b5060af806100396000396000f3fe60806040526004361060305760003560e01c80631b27274b1460355780633a7852381460715780634dec9b57146035575b600080fd5b348015604057600080fd5b50d38015604c57600080fd5b50d28015605857600080fd5b50605f6074565b60408051918252519081900360200190f35b605f5b60019056fea2646970667358221220188c1499dd33ba3a8221883471a78a67be5d60f1bc41e01ae8729ed43c4d9fc964736f6c6343000700003330643a1474657374436f6e7374616e74436f6e747261637440c7e3d28eb0c30270afa7bd95a32f90018094ebdc03\"}\n","privateKey":"2419e77042c9f9309f2479c962fdda2a069485f77331216efafe00bf954350da"}
    def gettransactionsign(self, transaction):
        url = "https://{}/wallet/gettransactionsign". format(self.httpNode)
        body =  json.loads(transaction)
        body["privateKey"] = self.key
        response = requests.post(url, json.dumps(body), headers = self.headers)
        return response.text

    # url: https://api.nileex.io/wallet/broadcasttransaction
    # body: {"visible":true,"signature":["0078a22f641aa2894f1ac042335c544f57744c0be60c2d6ace1b18bb1cad7d1169cfa71ce779e0d1186c771277c948678db8d3566394cbc602de4c8b478cbd2b01"],"txID":"068ac4f00044ee134d8677f8637ae51ca735dc2ce954bec23226c5d2b4da9125","contract_address":"41f7391173a06be57e4591f68e90f9f295262b9ad7","raw_data":{"contract":[{"parameter":{"value":{"owner_address":"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS","new_contract":{"bytecode":"608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029","consume_user_resource_percent":100,"name":"SomeContract","origin_address":"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS","abi":{"entrys":[{"inputs":[{"name":"key","type":"uint256"},{"name":"value","type":"uint256"}],"name":"set","stateMutability":"Nonpayable","type":"Function"},{"outputs":[{"name":"value","type":"uint256"}],"constant":true,"inputs":[{"name":"key","type":"uint256"}],"name":"get","stateMutability":"View","type":"Function"}]},"origin_energy_limit":100000}},"type_url":"type.googleapis.com/protocol.CreateSmartContract"},"type":"CreateSmartContract"}],"ref_block_bytes":"bae4","ref_block_hash":"513f674b753f4814","expiration":1624349355000,"fee_limit":1000000,"timestamp":1624349295996},"raw_data_hex":"0a02bae42208513f674b753f481440f8d79096a32f5add03081e12d8030a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e747261637412a3030a1541be16fd25b87f12bbec7ba29028f05471000582a71289030a1541be16fd25b87f12bbec7ba29028f05471000582a71a5c0a2b1a03736574220e12036b65791a0775696e743235362210120576616c75651a0775696e74323536300240030a2d10011a03676574220e12036b65791a0775696e743235362a10120576616c75651a0775696e743235363002400222fd01608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b2504002930643a0c536f6d65436f6e747261637440a08d0670fc8a8d96a32f9001c0843d"}
    def broadcastTransaction(self , transaction):
        url = "https://{}/wallet/broadcasttransaction". format(self.httpNode)
        response = requests.post(url, transaction, headers = self.headers)
        # print ("broadcast: ",response.text)
        return response.text

    def getaccountResource(self,account,visible = "true"):
        url = "https://{}/wallet/getaccountresource". format(self.httpNode)
        body = {"address": account, visible: visible}
        response = requests.post(url, json.dumps(body), headers = self.headers)
        # print ("getaccountresource: ",response.text)
        return response.text

    def getBlockByNum(self,number):
        url = "https://{}/wallet/getblockbynum". format(self.httpNode)
        body = {"num": number}
        response = requests.post(url, json.dumps(body), headers = self.headers)
        return response.text

    def getChainParameters(self):
        url = "https://{}/wallet/getchainparameters". format(self.httpNode)
        response = requests.get(url, headers = self.headers)
        return response.text

    def clearAbi(self,contractAddress,visible = "true"):
        url = "https://{}/wallet/clearabi". format(self.httpNode)
        body = {"owner_address": self.account,"contract_address": contractAddress,visible: visible}
        responseclear = requests.post(url, json.dumps(body),headers = self.headers).text
        # print("clearAbi: ",responseclear)
        responseSign = self.gettransactionsign(responseclear,self.key)
        responseBroad = self.broadcastTransaction(responseSign)
        sleep(3)
        assert json.loads(responseBroad).get("result") == True,"clearAbi failed!contractAddress:%s " % contractAddress

    def gettransactionbyid(self,txId):
        url = "https://{}/wallet/gettransactionbyid". format(self.httpNode)
        body = {"value": txId}
        response = requests.post(url, json.dumps(body), headers = self.headers)
        return response.text

    def createAccount(self):
        url = "https://{}/wallet/generateaddress". format(self.httpNode)
        response = requests.get(url, headers = self.headers)
        print (response.text)




# This file is a library file, you can call all the methods in this file.
# The function in this file is the underlying interface related to the contract.
def stringToHex(num):
    n = hex(int(num))
    print (n)
    return n[2:]

def hexTo64Hex(num):
    res = ""
    l = len(num)
    for i in range(0,64-l):
        res += "0"
    res += num
    # print (res)
    return res



if __name__ == '__main__':
    # print(getContract("TNtrTKmkKWoYYucELGjDRsAAqQcwwWHyAz"))
    # print(triggerConstantContract("TNtrTKmkKWoYYucELGjDRsAAqQcwwWHyAz","safeVault()","TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"))
    # print(TriggerSmartContract("TDPEv6sZj49KzR2jjdTZ7EQMFB3DPDoyWf","add_liquidity(uint256[3],uint256)",
    #                            "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640000000000000000000000000000000000000000000000000000000000000000",
    #                            0,"TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"))
    # hexTo64Hex(stringToHex("10000000000000000000000000000"))

    # resDict = triggerConstantContract("TPDMF7GVzivR6heo3PzN85HZFLoGScd9Bb", "rewardNextData(address)", "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS",\
    #                                   "true","0000000000000000000000006a6337ae47a09aea0bbd4faeb23ca94349c7b774")
    # res = resDict.get("constant_result")[0]


    # "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"
    account = "41BE16FD25B87F12BBEC7BA29028F05471000582A7"
    co = contractObject("api.nileex.io", account)
    # no constructor params
    # abi = '[{"constant":false,"inputs":[{"name":"key","type":"uint256"},{"name":"value","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"key","type":"uint256"}],"name":"get","outputs":[{"name":"value","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
    # bytecode = "608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029"
    # contractAddress = co.deployContract(abi,bytecode,"",100,"kkkkk",0,10)
    # # constructor params
    # abi = '[{"inputs":[{"internalType":"address","name":"add","type":"address"}],"stateMutability":"payable","type":"constructor"},{"inputs":[],"name":"get","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"add","type":"address"}],"name":"set","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"}]'
    # bytecode = "608060405260405161022d38038061022d8339818101604052602081101561002657600080fd5b8101908080519060200190929190505050806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506101a6806100876000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c80632801617e1461003b5780636d4ce63c146100a9575b600080fd5b61007d6004803603602081101561005157600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506100dd565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100b1610147565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000816000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690509056fea264697066735822122075eee6f8bd0505550b8373611021dfd1466b76c08b48661969ccdf8b4137901064736f6c63430007000033"
    # contractAddress = co.deployContract(abi,bytecode,"000000000000000000000000BE16FD25B87F12BBEC7BA29028F05471000582A7",100,"hhhjj",0,10)
    # print(co.triggerConstantContract(contractAddress,"get()","false"))
    # print(co.TriggerSmartContract(contractAddress,"set()",account,0,"false"))
    # print (co.getAccount(account,"false"))

    # print(co.gettransactionbyid("261effe806c3a9e2d7d5a1a4306160e5c4533f9e16afd4d42f0a985dbf47a3aa"))

    # # tr = tronObject()
    # print(tr.base58ToHex("TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS"))
    # print(tr.hexToBase58("41BE16FD25B87F12BBEC7BA29028F05471000582A7"))
    # print(co.gettransactioninfobyid("261effe806c3a9e2d7d5a1a4306160e5c4533f9e16afd4d42f0a985dbf47a3aa"))
    print(co.createAccount())