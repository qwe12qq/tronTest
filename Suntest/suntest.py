import os,sys

class parseFile():
    def __init__(self,sb,eb):
        self.block = "%s_%s"%(sb,eb)
        self.fileNameList = []
        self.typeAllPoolCountDict = {'10':{},'20':{},'30':{},'40':{},'50':{},'60':{}}
        self.standPoolCountDict = {'10':{},'20':{},'30':{},'40':{},'50':{},'60':{}}
        self.poolPrecisionDict = {'10':1e18,'20':1e6,'30':1e18,'40':1e6,'50':1e6,'60':1e17}

    def getFileName(self):
        for i in range(1,7):
            name = "allaccounttoken_1_%s_%s.txt" % (str(i*10) ,self.block)
            self.fileNameList.append(name)

    def integrateData(self):
        for ele in self.fileNameList:
            path = "rewards3211/"+ele
            type = ele.split("_")[2]
            f = open(path,'r').readlines()
            tmp_dict = {"BTCST-TRX":0,"SunUSDJ_TRXPool":0,"SunUSDT_TRXPool":0,"SunSUN_TRXPool":0,"SunETH_TRXPool":0,"SunWIN_TRXPool":0,"SunWBTT_TRXPool":0,"SunBTC_TRXPool":0,"SunJST_TRXPool":0,"jWIN":0,"jWBTT":0,"jETH":0,"jJST":0,"jSUN":0,"jTRX":0,"jUSDJ":0,"jUSDT":0,"jBTC":0}
            for line in f:
                line = line.strip().split("\t")
                name,address,count = line[0],line[1],line[-1]
                tmp_dict[name] += int(count)*24/self.poolPrecisionDict[type]
            self.typeAllPoolCountDict[type] = tmp_dict
        # print(self.typeAllPoolCountDict)

    def calcuStandAccure(self):
        f = open("rewards3211/standAccure", 'r').readlines()
        for ele in f:
            if "name" in ele:continue
            ele = ele.strip().split()
            name,c10 ,c20,c30,c40,c50,c60 = ele[0],ele[5],ele[1],ele[2],ele[3],ele[4],ele[6]
            self.standPoolCountDict["10"][name] = float(c10) * 7
            self.standPoolCountDict["20"][name] = float(c20) * 7
            self.standPoolCountDict["30"][name] = float(c30) * 7
            self.standPoolCountDict["40"][name] = float(c40) * 7
            self.standPoolCountDict["50"][name] = float(c50) * 7
            self.standPoolCountDict["60"][name] = float(c60) * 7
        # print (self.standPoolCountDict)

    def parRes(self):
        f = open("res3204",'w')
        s = "type\taddress\tcalcuValue\tstandValue\tDifference\n"

        for type,tmpdict in self.typeAllPoolCountDict.items():
            for address,value in tmpdict.items():
                s += "%s\t%s\t%s\t%s\t%s\n" %(type,address,str(value),
                                             str(self.standPoolCountDict.get(type).get(address)),
                                             str(self.standPoolCountDict.get(type).get(address)-value))
        f.write(s)

def main():
    startBlock = "28581837"
    endBlock = "28582053"
    pf = parseFile(startBlock,endBlock)
    pf.getFileName()
    pf.integrateData()
    pf.calcuStandAccure()
    pf.parRes()

if __name__ == '__main__':
    main()