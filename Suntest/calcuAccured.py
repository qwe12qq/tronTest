import os,sys
import xlrd,xlwt
import xlsxwriter


class tools:
    def __init__(self,startBlock,endBlock,dir,oldpoolsec,btcseconds,filename):
        self.sb = startBlock
        self.eb = endBlock
        self.dir = dir
        self.filename = filename
        self.oldPoolSecs = oldpoolsec
        self.btcstSecs = btcseconds
        self.sb_eb = "_{}_{}.txt".format(startBlock,endBlock)
        self.fileNameList,self.alterFileList = [],[]
        self.standAccuredDict,self.reportAccuredDict = {},{}
        # self.poolPrecisionDict = {'10':1e18,'20':1e6,'30':1e18,'40':1e6,'50':1e6,'60':1e17}
        self.poolPrecisionDict = {'10':1e6,'20':1e6,'30':1e6,'40':1e6,'50':1e18}
    def __cal(self,a,t):
        num = int(self.eb) - int(self.sb)
        if t == "60":
            m = float(a)/24/3600* self.btcstSecs;
        else:
            m = float(a)/24/3600* self.oldPoolSecs;
            m = float(a)/24/3600*3 * num;
        return round(m, 8)

    def __calBlock(self,a):
        m = float(a)/24/3600*3
        return round(m,8)

    def __handlePrecision(self,a,type):
        m = float(a)/float(self.poolPrecisionDict.get(type))
        return round(m,8)

    def getNamelist(self):
        d = {10:"TRX",20:"WBTT",30:"NFT",40:"WIN",50:"JST"}
        for i in range(1,len(d)+1):
            t = "1_{}".format(d.get(i*10))
            tmp = "{}alltoken_{}{}".format(self.dir,t,self.sb_eb)
            atmp = "{}alltoken_{}{}.new".format(self.dir,t,self.sb_eb)
            self.fileNameList.append(tmp)
            self.alterFileList.append(atmp)
        # print (self.fileNameList,self.alterFileList)

    def parseName2New(self):
        for ele in self.fileNameList:
            fr = open(ele,"r").readlines()
            print(ele)
            fw = open(ele+".new","w")
            st = ""
            # swicher = {              #定义一个map，相当于定义case：func()
            #     'TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP':"jTRX",'TGBr8uh9jBVHJhhkwSJvQN2ZAKzVkxDmno':"jSUN",
            #     'TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT':"jBTC","TXJgMdjVX5dKiQaUi9QobwNxtSQaFqccvd":"jUSDT",
            #     'TL5x9MtSnDy537FXKx53yAaHRRNdg9TkkA':"jUSDJ",'TWQhCXaWz4eHK4Kd1ErSDHjMFPoPc9czts':"jJST",
            #     'TR7BUFRQeq1w5jAZf1FKx85SHuX6PfMqsV':"jETH",'TUY54PVeH6WCcYCd6ZXXoBDsHytN9V5PXt':"jWBTT",
            #     'TRg6MnpsFXc82ymUPgf5qbj59ibxiEDWvv':"jWIN",'TMypaK8uiihyrQfJRAQGQHM9ZKiDdYx1AR':"SunSUN_TRXPool",
            #     'TDB8Y2WMMeRivgxdsYniAyrGNWdCQisCvQ':"SunJST_TRXPool",'TWPcaMKwJAqHk7Ta3fYdHaHeBU2kES9TLH':"SunWBTT_TRXPool",
            #     'TLCWfcYqmYZ6anvfq8AVPSiUuvRKwTyQx5':"SunBTC_TRXPool",'TWnTQ5grjn4nAJThs4JVGcyCYzzACd4ycq':"SunUSDT_TRXPool",
            #     'TLNBj6KNXMxcQutEPjgqotA6Wvr5mEVNd6':"SunUSDJ_TRXPool",'TGTN3wq6bDNMxvzYZrJqq6irJ9M1HWYAxX':"SunWIN_TRXPool",
            #     'TWKrCJCaeMzvixk8y1QLNbfwNVEjZz3CYF':"SunETH_TRXPool",'TL5uiT7s5kYwJJSdy4qxv2qbjiDZyhQp6i':"BTCST_TRX",
            #     'TPX6nmRUqCQXGsAF9p64wLC4tgVE3JR9gR':'TUSD_TRX','TV1nW5ay1JWaDrNg9xJpzp78W3CFiGwERd':"TUSD_TRX",
            #     'TSXv71Fy5XdL3Rh2QfBoUu3NAaM4sMif8R':'jTUSD'
            # }
            swicher = {
                'TVn5SqEfrKd2aeoQm1ZWioH458KM3Vb5iD':'USDT-TRX','TRpbsXviyETj1ngrgYSjEympGx8geA1sFW':'USDJ-TRX',
                'TPX5DGqK8ALCxFgWZompkGL5AUhycWL6xi':'TUSD-TRX','TCBNm3ATvioeaLHLceRuA62usrTJS6KXWq':'BTC-TRX',
                'TK2sKJP8Nr8xRPipbVckqnX6t9HBW6adBR':'ETH-TRX','TPDMF7GVzivR6heo3PzN85HZFLoGScd9Bb':'WBTT-TRX',
                'TKKMuQuMRrpcHYPoP55zmgkLwGgd1TMK2N':'NFT-TRX','TBTK7orRXZxv9BLR7J22RDY2CY4Pv2Fkwm':'WIN-TRX',
                'TUp1BWfAZidkNbWkoiCjJcf4ctE4PAR2Rg':'JST-TRX','TRg6MnpsFXc82ymUPgf5qbj59ibxiEDWvv':"jWIN",
                'TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP':"jTRX",'TPXDpkg9e3eZzxqxAUyke9S4z4pGJBJw9e':"jSUNNEW",
                'TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT':"jBTC","TXJgMdjVX5dKiQaUi9QobwNxtSQaFqccvd":"jUSDT",
                'TL5x9MtSnDy537FXKx53yAaHRRNdg9TkkA':"jUSDJ",'TWQhCXaWz4eHK4Kd1ErSDHjMFPoPc9czts':"jJST",
                'TR7BUFRQeq1w5jAZf1FKx85SHuX6PfMqsV':"jETH",'TUY54PVeH6WCcYCd6ZXXoBDsHytN9V5PXt':"jWBTT",
                'TSXv71Fy5XdL3Rh2QfBoUu3NAaM4sMif8R':'jTUSD',"TMbf5ZMK3UNthUDbQsYe8w8wQVJh4FwnpZ":"USDC-TRX",
                'TFpPyDCKvNFgos3g3WVsAqMrdqhB81JXHE':'jNFT','TNSBA6KvSvMoTqQcEgpVK7VhHT3z7wifxy':'jUSDC'
            }

            for l in fr:
                if l == "\n":continue
                lines = l.split("\t")
                lines[0] = swicher.get(lines[1])
                print (lines)
                st += "\t".join(lines)
            fw.write(st)

    def getReportAccur(self):
        # d = {"SUN":10,"TRX":20,"JST":30,"WBTT":40,"WIN":50,"BTCST":60}
        d = {"TRX":10,"WBTT":20,"NFT":30,"WIN":40,"JST":50}
        for ele in self.alterFileList:
            flines = open(ele,"r").readlines()
            type = d.get(ele.split("_")[2])
            self.reportAccuredDict[type] = {}
            for line in flines:
                l = line.replace(":"," ").split()
                # print (l)
                self.reportAccuredDict[type][l[0]] = self.__handlePrecision(l[5],str(type))
        # print (self.reportAccuredDict)

    def getStandAccure(self):
        flines = open("justswapSpeed","r").readlines()
        for line in flines:
            l = line.strip().split()
            if "name" in l:
                typeList = l[1:]
                self.standAccuredDict = dict(zip(typeList,[{},{},{},{},{},{}]))
                continue
            else:
                self.standAccuredDict["10"][l[0]] = l[1]
                self.standAccuredDict["20"][l[0]] = l[2]
                self.standAccuredDict["30"][l[0]] = l[3]
                self.standAccuredDict["40"][l[0]] = l[4]
                self.standAccuredDict["50"][l[0]] = l[5]
                # self.standAccuredDict["60"][l[0]] = l[6]
            # print (self.standAccuredDict)

    def parseResult2Excel(self):
        workbook = xlsxwriter.Workbook(self.filename)
        workfomat = workbook.add_format()
        workfomat.set_align('left')
        sh = workbook.add_worksheet('收益')
        sh.set_default_row(20)
        sh.set_column(0, 20, 20)
        datas = []
        workfomat.set_bold(True)
        heads = ['name',"type", "速度/日","速度/块",'报表数据', '理论数据', '理论数据-报表数据','差值/理论数据','差值/块速度']
        sh.write_row('A1', heads, workfomat)
        for typet,values in self.standAccuredDict.items():
            for name,val in values.items():
                if float(val) < 0.1:continue
                # print(self.reportAccuredDict)
                reportvalue = self.reportAccuredDict.get(int(typet),{}).get(name,0)
                standValue = self.__cal(val,typet)
                speedBlock = self.__calBlock(val)
                gap = standValue - reportvalue
                gapRatio = gap / standValue
                gapblock = gap / speedBlock
                tp = [name,typet,val,speedBlock,reportvalue,standValue,gap,gapRatio,gapblock]
                datas.append(tp)
        for i in range(len(datas)):
            l = str(i+2)
            sh.write_row('A'+ l , datas[i], workfomat)
        sh.freeze_panes(1,0)
        workbook.close()
        print("excel success!")

def main():
    t = tools("33789995","33991418","reward0924/",604800,604800,"test0924.xlsx")
    t.getNamelist()
    t.parseName2New()
    t.getStandAccure()
    t.getReportAccur()
    t.parseResult2Excel()

if __name__ == '__main__':
    main()