from web3 import Web3, HTTPProvider
from time import sleep
from web3.middleware import geth_poa_middleware

class EthObject():
    '''
    INFURA 不支持web3.eth.sendTransaction方法
    '''
    def __init__(self,addr,privateKey,INFURA_api):
        self.addr = addr
        self.privateKey = privateKey
        self.web3 = Web3(HTTPProvider(INFURA_api))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def getBalance(self,addr):
        return self.web3.eth.get_balance(addr)

    def getContractInstance(self,address,abi):
        contract_instance = self.web3.eth.contract(address=address, abi=abi)
        return contract_instance

    def getBlockNumber(self):
        return self.web3.eth.block_number

    def getPendingNonce(self,addr):
        return self.web3.eth.getTransactionCount(addr, 'pending')

    def getCotractAllFunctions(self,contractInstance):
        return contractInstance.all_functions()

    def getLogs(self,contractInstance,txId,method):
        tx_receipt = self.web3.eth.get_transaction_receipt(txId)
        str = "contractInstance.events.{}".format(method)
        rich_logs = eval(str).processReceipt(tx_receipt)
        print(rich_logs)

    def getTransaction(self,hash):
        return self.web3.eth.get_transaction(hash)

    # 可以查看到具体交易数据
    def getTransactionReceipt(self,hash):
        return self.web3.eth.get_transaction_receipt(hash)

    def getBlockTransaction(self,block):
        return self.web3.eth.get_transaction_by_block(block, 0)

    def toHex(self,content):
        return self.web3.toHex(text=content)

    def toText(self,hex):
        return self.web3.toText(hexstr=hex)

    def deployContract(self,abi,byteCode,constructorParam):
        contract = self.web3.eth.contract(abi=abi,bytecode=byteCode)
        str = "contract.{}".format(constructorParam)
        construct_txn =  eval(str).buildTransaction({
            'from': self.addr,
            'nonce': self.web3.eth.getTransactionCount(self.addr),
            'gas': 5000000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice': self.web3.eth.gasPrice})

        signed = self.web3.eth.account.signTransaction(construct_txn,private_key=self.privateKey) # 交易签名
        tx_id = self.web3.eth.sendRawTransaction(signed.rawTransaction) # 交易发送
        # print("deploy contract hex:",tx_id.hex())
        sleep(30)
        contract_addr = self.web3.eth.getTransactionReceipt(tx_id.hex()).contractAddress # 通过交易 id 查询合约地址
        return contract_addr

    def callConstantContract(self,contractInstance,method):
        str = "contractInstance.functions.{}.call()".format(method)
        res = eval(str)
        return res

    def callSmartContract(self,contractInstance,method):
        str = "contractInstance.functions.{}".format(method)
        tx = eval(str).buildTransaction({'gas': 5000000,
                                         'value':Web3.toWei(0,'ether'),
                                         'gasPrice': self.web3.eth.gasPrice,
                                         'from': self.addr,
                                         'nonce': self.web3.eth.getTransactionCount(self.addr)}) # 构造交易

        signed = self.web3.eth.account.signTransaction(tx,private_key=self.privateKey) # 交易签名
        tx_id = self.web3.eth.sendRawTransaction(signed.rawTransaction) # 交易发送
        print("callSmartContract hex:",tx_id.hex())
        sleep(30)
        # self.getLogs(contractInstance,tx_id,"Set()")


if __name__=="__main__":
    INFURA_api = 'https://goerli.infura.io/v3/30c968d252ba450d80db50d6b0545e83'
    priv_key = "0x127109F1B8FEC8CFAB6A3D4DCE13BBD748195BFD0B08F12FB2776446CC09A11F" # 账户私钥
    my_addr = "0xbe16fD25b87F12Bbec7BA29028f05471000582A7" # 账户地址
    ob = EthObject(my_addr,priv_key,INFURA_api)

    # print(ob.toHex("ooo99900"))
    # print(ob.toText("0x636f776dc3b6"))
    ob.getBalance(my_addr)
    ob.getBalance("0x3DFF61719256D9d48baE6a922f5eB0aeF70ff5D9")
    ob.transferETH(my_addr,priv_key,"0x3DFF61719256D9d48baE6a922f5eB0aeF70ff5D9",100)
    ob.getBalance(my_addr)
    ob.getBalance("0x3DFF61719256D9d48baE6a922f5eB0aeF70ff5D9")
    # construct 没有入参
    # abi = "[{\"constant\":false,\"inputs\":[],\"name\":\"callme\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"isComplete\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]"
    # bycode = "608060405260008060006101000a81548160ff02191690831515021790555034801561002a57600080fd5b5060e8806100396000396000f3006080604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063a3c8e39314604e578063b2fa1c9e146062575b600080fd5b348015605957600080fd5b506060608e565b005b348015606d57600080fd5b50607460aa565b604051808215151515815260200191505060405180910390f35b60016000806101000a81548160ff021916908315150217905550565b6000809054906101000a900460ff16815600a165627a7a72305820b8fa6a8efd9ae9f8ec9940375e07b12a11977fd6bee3e4f923139ac0e535609e0029"
    # contractAddress = ob.deployContract(abi,bycode,'constructor()')
    #construct 有参数
    # abi = "[{\"constant\":false,\"inputs\":[{\"name\":\"n\",\"type\":\"string\"}],\"name\":\"set\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"get\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"name\":\"s\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"indexed_from\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"n\",\"type\":\"string\"}],\"name\":\"Set\",\"type\":\"event\"}]"
    # bycode = "608060405234801561001057600080fd5b506040516104ab3803806104ab833981018060405281019080805182019291905050508060009080519060200190610049929190610050565b50506100f5565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061009157805160ff19168380011785556100bf565b828001600101855582156100bf579182015b828111156100be5782518255916020019190600101906100a3565b5b5090506100cc91906100d0565b5090565b6100f291905b808211156100ee5760008160009055506001016100d6565b5090565b90565b6103a7806101046000396000f30060806040526004361061004c576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680634ed3885e146100515780636d4ce63c146100ba575b600080fd5b34801561005d57600080fd5b506100b8600480360381019080803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919291929050505061014a565b005b3480156100c657600080fd5b506100cf610234565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561010f5780820151818401526020810190506100f4565b50505050905090810190601f16801561013c5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101609291906102d6565b507fde696604ac839ef8a5d0fcb2310ea48463357a6247e0d961d77c41d136a5d9463382604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200180602001828103825283818151815260200191508051906020019080838360005b838110156101f65780820151818401526020810190506101db565b50505050905090810190601f1680156102235780820380516001836020036101000a031916815260200191505b50935050505060405180910390a150565b606060008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102cc5780601f106102a1576101008083540402835291602001916102cc565b820191906000526020600020905b8154815290600101906020018083116102af57829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061031757805160ff1916838001178555610345565b82800160010185558215610345579182015b82811115610344578251825591602001919060010190610329565b5b5090506103529190610356565b5090565b61037891905b8082111561037457600081600090555060010161035c565b5090565b905600a165627a7a72305820ba5ea34ac5e92cf5b8601ff0a9466d76b48b786812a483b329229e85a07ddc520029"
    # contractAddress = ob.deployContract(abi,bycode,'constructor("aadd")')
    # print(contractAddress)

    # contractAddress = "0xAaCA43E952006428AB8fC990e4c7d71bf0c5951e"
    # contract_instance = ob.getContractInstance(contractAddress,abi)
    # print(ob.callConstantContract(contract_instance,"get()"))
    # ob.callSmartContract(contract_instance,'set("iiii")')
    # # ob.callSmartContract(contract_instance,'set()')  #如果没有入参 可以直接这样调用
    # print(ob.callConstantContract(contract_instance,"get()"))
