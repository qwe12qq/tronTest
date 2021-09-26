import os,sys
import json
import requests

class case2():
    def __init__(self):
        self.accountList = ["TS8v54PXszgnktpBm1JtzfXrDV7C4L8CwM","TLipJxwgDbn7FaQCnECxiYdxFTBhshLiW3","TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS","TDQsxPhq9bgmnw9CeDSrXsYjqt2rb1b3pg","TQRj3keAZdS9mUWqReMFuYRhAZdEZuPoHc","TVNevinkBb9JytBHhK2ZMsnWX5sWqJu9fx","TKpkpvcGriyNoiqhfBMLBGehmyXcDkDtER","TFDP1vFeSYPT6FUznL7zUjhg5X7p2AA8vw","TLLpedRL3d7c3u5SiHq7xD5UgfmtFjQKt3","TTZLtS7QUiCG83kcqFA1jw1AVJC8LvszdR","TWiSvJSBpnNv1Qi7MContRnWxfMJZYwoQx","TTQjvjhipmFCmChYQmNLo79S6UF8Fz63VE","TThCay1zZBdv6SN6DkbirV3uArGUwdkJTE","TN21Wx2yoNYiZ7znuQonmZMJnH5Vdfxu78","TFtzWUH2oBXTXZfUSuS7CZJcj2BS2zr9Cq","TEcHv5BPtcvaGVrnBWZS4WucRU1YcGbLuo","TUevaYJnJEE61jAbHbJtfUZATwKTDeTbdo","TAXqycjb1sYZPsaTEEvHirhax5Q5fkghMx","TM8CFhGEm4YP6t5WNsSamdBCw3tycQaiMn","THoAJaTCfpsskshr6cWRVvfUX9MCaZDKP1","TKGRE6oiU3rEzasue4MsB6sCXXSTx9BAe3","TBfAnqSQpFdwRbMTo2JgQZLMXi76wYgggB","TFK9zdcdgW8FjYvS48Bfcwu2jHzf41rUiQ","TVGcrhDcEWvSBsQdtLZ2XoMVLqaD8SRRJR","TE4CeJSjLmBsXQva3F1HXvAbdAP71Q2Ucw","TPXXPgzEWFKy1bQStAm8n9NCUqQD8FsmGX","TS8fyGssAxgBttmezCis9o3zz3jir5ysp9","TPMzoXfgrgTCfw8N6LZKLukbG3ujNzQNGC","TDf3JZtjDeEqsFdPGp6vT9meG3JxMwmXwA","TTG8u8fUKqJwMtB59ppaWqgFVGDb5ojWPU","THph9K2M2nLvkianrMGswRhz5hjSA9fuH7","TQ48z1p3kdQeZrf5Dc62U88bsbhvRJJQFn","TXTNcgJHD9GPfpiTbSG2VGtfdfii9VcpEr","TPyVMgQ9gCpnP6oyHpKY2kEYPDCXm4KY7y","TEy7ZwNHbwE5pTLCPmb7cZpcoRVej785zA","TQ9gXwoLcLi6W5gV5RjRykVuLVYTDY54nK","TU2YbajwkDnrSUwu858kvMJtLaYZwVoKGC","TM9LH7NzuikEXT4Ac5swr4XVa1w1DSV5NH","TH48niZfbwHMyqZwEB8wmHfzcvR8ZzJKC6","TGLrbp8jjBHdAGaera34fGwGS32Vm6Ly79","TRqduDBRMyKBkadGY2JCneCuo3T1mTfJzM","TYmUhWaHCJw5edMDgvM7n2YCafWmshWpU5","TTfj8fUpzkAbt23vY78tMM4QZuEt2kM7YR","TRAiS5SxmiNdVDUDyM2NbpW1sDKkLQuC5L","TYhmxgsmxc5nsD5mhU78VBEb2pzoJmCDJa","TV75jZpdmP2juMe1dRwGrwpV6AMU6mr1EU","TXxhLXT1iM5hfKYWUiTfV4cVT3Xnp7k1dN","TUVpKHf9SZkNwqogUBBugsbSXuwrWH8U3k","TB6Ed7FucoQDqZ57oooL7ZvwB4A6SExYfs","TJBE61UKoXkZy2LEJQcjH3Awm8sqdBJioC","TXUV9XyBihaQ9bD6HB4HcAUoy8EGn8eGxj","TLypJm1rXcohwiEyUNnJNqEh339fwjKLkG","THGhxiW84rC4Dv4RxGXSYXRHHLBmrhgw7n","TDsLZoTfrnN4cSzsqAatYn9PRhYEwR1z6z","TX74o6dWugAgdaMv8M39QP9YL5QRgfj32t","TCmuKb5NgKgj2bv8TNLALCdfSwJSrzNTvC","TRMT8PEeDM61HWHs1iyop2taSxJfwbToub","TW785YTMsdZfMxrrNFxofWb9CAN9SeDzBC","TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL","TBYa3D5SndWnHDVXqE3qSztsw5H4GhNk3L","TYJR5eYSmkEysQxbiF5wSoF68UtGTobvVL","TJJeCr6Csuj2gafDTapGpKWvBk8a1ycZTq","TQUsaH7DzTAPQEVsUvQsVyzvwqwT2p7WEm","TQa7aSuHe3CyD44QhFLMmtSLt5oyeUJfz9","TEtG9fnVi2qythiog6owPrg4sD9rwFBQBN","TM18kcZVW3ppq9ZLbHiGtRBKamAFC4rYtN","TRM11TZjzC8Gksria7tpYZvHEWpGW2T68r","TW6omSrQ1ZK37SwSvTQD5Cnp2QbEX2zDVZ","TVsTKPtzucizWWfeZQKRXa7eEVkVDxkCTc","TEf1UDgomx2CQxhvU1Z1WhNJXg2YvCcjTU","TSPrmJetAMo6S6RxMd4tswzeRCFVegBNig","TA1g2WQiXbU5GnYBTJ5Cp22dvSjT3ug9uK","TGuAfXhPAZ3ZRFzxhvtgyXFMEEYF9g1tVG","TL7o4tJ3AGLoSQ3wbBEUq9UmduwH4CZqAB","TWniJeCRQFm4CAXzk6UL96xfBi6e6rpMGM","TTTXHEymRS3YHPYoogkQewYX6e1EMQnTTT","TFVdVgg4pbkKrPJXik1rfkbNhK1WgqXuB7","TJtAFmv2KB5GEhAm9KVZcm2HAwiE7nuEPy","TVYYUE5EtBzP5TUeRdX2qpvbcQ9YvMXRZL","TFSLatrogA3a4z185ACqtFHxwHtN7WQy1B","TMny11y54r54kyHHYzZGC5iEGKzUEw2dc4","TT8KFZLqBxdBUpwVyPbUeBVpSXD6zzf59p","TAYzcfLovWdV83g25Apfd7BA67J44D5z5M","TJeHToUZa5xaq84o9RqEsF6MvptF3F5V6s","TSvW8WqPe2GxR7kqeAEs8rFTcgZQ4V7H6G","TAnMMFHbRcU4jxbcreewCfRzMCjBz45CDe","TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ","TA81nE2qqWNwEAAqLYSi8w4h2eXTsZMLos","THN9YkeSQiV5AmUuN5V9hrajdqHyr8mm22","TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz","TS8o6WcHroSnzWNt4AiserAuVkye5Msvcm","TXdXbzjBj1X4w3br44Rh629qsbpxXmv8sf","TPVkPQ3gmRF6ZWAqThJjnsnS6Qzcxcmwx1","TLCEXuCquPcrPq5H1nUkUfCd2kG1RmYiyL","TRxXEwPDCUwS9bB9d9tz2QawkmPLkLUpEF","TWuPoiLwpU7bJ1Wu68vtWZQ8HQCmYXet93","TPkF7F4YUHjVvteMLDpv7Pf2rqeMTp5MCQ","TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA","TCrVRNYdngEuDTCMQHuWFT1uRansbk5DoC","TG3Bm5oPtXbyEc3K85ssMxDfFRik7A9g7A","TNr81bP6H84b3VJrakbxAPS9nFReBXuUYJ","TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs","TJyjQjoQ8xzJkkGgHEiAc9KohG29BsfSCL","TNDNLhhwW8NwdFxAYLXSdY6mQShWCa1aje","TBtoB9XMmL2uFsoXYVvgnh2yTK9Mx6DCbw","TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs","TQyjkYcUWTCiyqd6FdREQw8QWx2Tkhr8iz","TMYo7KqjzVdh7wPmrTPaN6EnNXEsfPyTKe","TYhwGbJMLiweKkgJassfJmiGy4EZJzhsid","TJhAWh24zFMtTSWZf9iiN3j1GMae4xeYZT","TMEKAfwpJLGSFKbrDDveCQFE9KD95JqPHD","TT39eb1P13eGTnG5ryjQv74vNMXK5n4u6A","TXxoFCgcE2tKoK3meZyL6qen9ga5YHwQZA","TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf","TAeRTA5w2vXfm4m2wS9m5LRoiJoejHUEW3","TPz7T4sei4b8vqzYNMGzSYu9X6VdMFXzRp","TUiQA1W9FHKuU11AEfZL7MkqUkTYEg15tQ","TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK","TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj","TRW6iXeYKLqvzYc1YGweRwjYDwsmSpfRw7","TGaudD8M1jN6TAvsWo4qNH7ogabK69G8yZ","TPCWVYgaFLBVYN4YmzKGvDfcpFrg8xKyFy"]
        self.zapperDict,self.yieldInfosDict = {},{}


    def yieldInfos(self):
        for account in self.accountList:
            tmp_dict = {}
            url = "http://123.56.166.152:10088/justlend/account?addr=%s&config=TDchKqQ8T2BhGfL7m2DfWfxp5eqa1we5hu$0$14,TTUtHMoRLR97C3kd6gyGPWb1ReCWDcRAyA$0$14,TTYKZf1Vv3sKED5LSKGh9Yi2XwJxam9nqj$0$14,TSdWpyV2Z8YdJmsLcwX3udZTTafohxZcVJ$0$14,TJRXoWa5CiG7ZRf36ncEXDLUoMbEuH3ZJs$0$14,TXjnpsP7FWCGZWzrFbXsQcpgyKd26v45dK$0$14,TCby9165NKLydYDJEQ1RTUdJ3VoFXq8VVs$0$14,TDYhBGVRwRCyvnfsnLrwtj1xWEsoPKVWKz$0$14,TJg1msVTDbv5wma5t5wDJKqDHAH4BzC85i$0$14,TCmJeP41ySJmyehWCyJoeWJuLdZM4bW9KA$0$14"%account
            resLend = requests.get(url).text
            res = json.loads(resLend)
            assers = res.get("data",{}).get("assetList",[])
            for ele in assers:
                jtokenAddress = ele.get("jtokenAddress","")
                account_entered = ele.get("account_entered",-1)
                account_depositJtoken = ele.get("account_depositJtoken","")
                account_borrowBalance = ele.get("account_borrowBalance","")
                exchangeRate = ele.get("exchangeRate",0)
                collateralDecimal = ele.get("collateralDecimal",0)
                tmp_dict[jtokenAddress] = {"account_entered": account_entered,"account_depositJtoken":account_depositJtoken,"account_borrowBalance":account_borrowBalance,"exchangeRate":exchangeRate,"collateralDecimal":collateralDecimal}
            self.yieldInfosDict[account] = tmp_dict
        # print(self.yieldInfosDict)


    def zapper(self):
        for account in self.accountList:
            tmp_dict = {}
            url = "http://123.56.166.152:10088/zapper/lend/account?account=" + account
            resZapper = requests.get(url).text
            res = json.loads(resZapper)
            assers = res.get("data",{}).get("assetList",[])
            for ele in assers:
                jtokenAddress = ele.get("jtokenAddress","")
                account_entered = ele.get("account_entered",-1)
                account_depositJtoken = ele.get("account_depositJtoken","")
                account_borrowBalance = ele.get("account_borrowBalance","")
                account_deposited = ele.get("account_deposited","")
                account_deposited_trx_value = ele.get("account_deposited_trx_value","")
                account_borrow_trx_value = ele.get("account_borrow_trx_value","")
                exchangeRate = ele.get("exchangeRate",0)
                collateralDecimal = ele.get("collateralDecimal",0)
                assetPrice = ele.get("assetPrice",0)
                tmp_dict[jtokenAddress] = {"account_entered": account_entered,"account_depositJtoken":account_depositJtoken,"account_borrowBalance":account_borrowBalance,"account_deposited":account_deposited,"account_deposited_trx_value":account_deposited_trx_value,"account_borrow_trx_value":account_borrow_trx_value,"exchangeRate":exchangeRate,"collateralDecimal":collateralDecimal,"assetPrice":assetPrice}
            self.zapperDict[account] = tmp_dict
        # print(self.zapperDict)

    def squre(self,times):
        res = 1
        for i in range(times):
            res = res * 10
        return res

# account_deposited = jtoken数量 * 兑换率/1e18
# account_deposited_trx_value = account_deposited * assetPrice/1e18
    def resParse(self):
        for account in self.zapperDict:
            zapperVal = self.zapperDict[account]
            yieldVal = self.yieldInfosDict[account]
            # print(zapperVal.keys(),yieldVal.keys())
            assert set(zapperVal.keys()) == set(yieldVal.keys()),"keys not equall!"
            for jtoken,value in zapperVal.items():
                print(account,jtoken)
                print("account_entered: ",value["account_entered"] , yieldVal[jtoken]["account_entered"])
                print("account_depositJtoken: ",value["account_depositJtoken"] , yieldVal[jtoken]["account_depositJtoken"])
                print("exchangeRate:",value["exchangeRate"] , yieldVal[jtoken]["exchangeRate"])
                print("account_borrowBalance:",value["account_borrowBalance"] , yieldVal[jtoken]["account_borrowBalance"])
                print("collateralDecimal: ",value["collateralDecimal"], yieldVal[jtoken]["collateralDecimal"])
                assert value["account_entered"] == yieldVal[jtoken]["account_entered"],"account_entered check failed!"
                assert value["account_depositJtoken"] == yieldVal[jtoken]["account_depositJtoken"],"account_depositJtoken check failed!"
                # assert value["account_borrowBalance"] == yieldVal[jtoken]["account_borrowBalance"],"account_borrowBalance check failed!"
                assert value["exchangeRate"] == yieldVal[jtoken]["exchangeRate"],"exchangeRate check failed!"
                assert value["collateralDecimal"] == yieldVal[jtoken]["collateralDecimal"],"collateralDecimal check failed!"
                account_deposited = int(value["account_depositJtoken"])*int(value["exchangeRate"])/1e18
                print("account_deposited: ",int(account_deposited),value["account_deposited"])
                assert int(account_deposited) - int(value["account_deposited"]) < 1e8,"account_deposited failed!"
                print(self.squre(int(value["collateralDecimal"])))
                account_deposited_trx_value = int(value["account_deposited"]) *int(value["assetPrice"])/1e18
                print("account_deposited_trx_value: ",int(account_deposited_trx_value),value["account_deposited_trx_value"])
                assert int(account_deposited_trx_value) - int(value["account_deposited_trx_value"]) <2,"account_deposited_trx_value failed!"
                account_borrow_trx_value = int(value["account_borrowBalance"])*int(value["assetPrice"])/1e18

                print("account_borrow_trx_value: ",account_borrow_trx_value,value["account_borrow_trx_value"])
                assert int(account_borrow_trx_value) - int(value["account_borrow_trx_value"]) < 2,"account_borrow_trx_value failed!"

def main():
    op = case2()
    op.yieldInfos()
    op.zapper()
    op.resParse()

if __name__ == '__main__':
    main()