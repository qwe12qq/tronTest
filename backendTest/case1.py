import os,sys
import json,requests,re
import utils.mysqlOperation as mysql
import utils.contractInteractive as contractOperate
import subprocess


class case1():
    def __init__(self,host,port,user,pw,db):
        self.db = mysql.mysqlOperate(host,port,user,pw,db)
        self.db.connect()
        self.accountExchanges = {}
        self.conOp = contractOperate.contractObject("api.nileex.io", "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS")


    def getSampleAccount(self):
        cmd = 'select user_address from `swap_liquidity_user` group by `user_address` order by count(*) desc;'
        resList = self.db.selectMysql(cmd)

        for account in resList[300:]:
            if "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb" == account[0]:continue
            if account[0] not in self.accountExchanges.keys():
                self.accountExchanges[account[0]] = {}
            cmd = 'select exchange_address from `swap_liquidity_user` where user_address = "{}";'.format(account[0])
            exchangeList = self.db.selectMysql(cmd)
            for ex in exchangeList:
                cmd = 'select token_symbol from `swap_exchange` where address="{}";'.format(ex[0])
                nm = self.db.selectMysql(cmd)
                if len(nm) == 0:continue
                self.accountExchanges[account[0]][ex[0]] = "S-%s-TRX"%nm[0][0]
        # print((self.accountExchanges))

    # check return address and name
    def swapLiquidity(self):
        baseurl = "http://123.56.166.152:10088/zapper/swap/liquidity?account="
        for key, value in self.accountExchanges.items():
            print (key)
            url = baseurl + key
            res = requests.get(url).text
            res = json.loads(res)
            assert len(res["data"]) == len(value),"account:%s data length is failed!"%(key)
            for ele in res["data"]:
                name = ele["name"]
                address = ele["address"]
                price = float(ele["price"])
                balance = float(ele["balance"])
                val = float(ele["value"])
                print("接口返回：price :%s，balance:%s，val:%s"%(price,balance,val))
                assert address in value.keys() ,"account:%s,contractaddress:%s is not in tables!"%(key,address)
                assert name == value[address],"account:%s, contractaddress:%s,name:%s name check is failed! "%(key,address,name)
                bal = self.checkBalance(address,key)
                assert balance == bal,"account:%s,contractaddress:%s balance check failed!"%(key,address)
                pr = self.checkPrice(address,key)
                assert price - pr < 0.1 or price == pr,"account:%s, contractaddress:%s ,price:%s ,pr:%s check is failed! "%(key,address,price,pr)
                valcal = price * balance/1e6
                print("计算：：price :%s，balance:%s，val:%s"%(pr,bal,valcal))
                assert valcal - val < 0.001,"value check is failed! "

    def checkBalance(self,contractAddress,accountAddress):
        host = "123.56.3.74"
        port = 3306
        user = "root"
        pw = "1234"
        db = "tronlink_trc20"
        dblink = mysql.mysqlOperate(host,port,user,pw,db)
        dblink.connect()

        cmd = "java -jar tronlink-mysql-query.jar " + accountAddress
        num = re.findall("[0-9].*?",os.popen(cmd).read())
        num = "".join(num)
        tableName = "balance_info_trc20_" + num
        sql = 'select balance from {} where token_address="{}" and account_address = "{}"'.format(tableName,contractAddress,accountAddress)
        resbal = dblink.selectMysql(sql)
        # print(sql,resbal)
        balance = resbal[0][0]
        return float(balance)


    # price = 池子内的trx的美元价值 * 2 / （lp代币的 totalSupply/1e6）
    def checkPrice(self,contractAddress,accountAddress):
        res = self.conOp.getAccount(contractAddress)
        res = json.loads(res)
        balance = res.get("balance",0.0)/1e6
        # print(contractAddress,balance)

        resT = self.conOp.triggerConstantContract(contractAddress,"totalSupply()")
        constant_result = resT.get("constant_result",0.0)[0]
        totalsupply = int(constant_result,16)
        # print(balance,totalsupply,"-----")
        if totalsupply == 0:
            return 0.0
        price = balance * 2 / (totalsupply/1e6)
        return float(price)

def main():
    host = "123.56.166.152"
    port = 3306
    user = "defi"
    pw = "wEJdXe3LIsClKpk6"
    db = "defi-swapqa"
    op = case1(host,port,user,pw,db)
    op.getSampleAccount()
    op.swapLiquidity()


if __name__ == '__main__':
    main()