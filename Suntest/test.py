import os,sys

def getFileName(st,et):
    fileNameList = []
    blcok = "%s_%s"%(st,et)
    for i in range(1,7):
        name = "alltoken_1_%s_%s.txt" % (str(i*10) ,blcok)
        fileNameList.append(name)
    return fileNameList

def parse(fileNameList):
    for ele in fileNameList:
        fr = open("debugReward31/"+ele,"r").readlines()
        fw = open("debugReward31/1"+ele,"w")
        st = ""
        for l in fr:
            lines = l.split("\t")
            # print (lines)
            if lines[1] == "TE2RzoSV3wFK99w6J9UnnZ4vLfXYoxvRwP":
                lines[0] = "jTRX"
            elif lines[1] == "TGBr8uh9jBVHJhhkwSJvQN2ZAKzVkxDmno":
                lines[0] = "jSUN"
            elif lines[1] == "TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT":
                lines[0] = "jBTC"
            elif lines[1] == "TXJgMdjVX5dKiQaUi9QobwNxtSQaFqccvd":
                lines[0] = "jUSDT"
            elif lines[1] == "TL5x9MtSnDy537FXKx53yAaHRRNdg9TkkA":
                lines[0] = "jUSDJ"
            elif lines[1] == "TWQhCXaWz4eHK4Kd1ErSDHjMFPoPc9czts":
                lines[0] = "jJST"
            elif lines[1] == "TR7BUFRQeq1w5jAZf1FKx85SHuX6PfMqsV":
                lines[0] = "jETH"
            elif lines[1] == "TUY54PVeH6WCcYCd6ZXXoBDsHytN9V5PXt":
                lines[0] = "jWBTT"
            elif lines[1] == "TRg6MnpsFXc82ymUPgf5qbj59ibxiEDWvv":
                lines[0] = "jWIN"
            elif lines[1] == "TMypaK8uiihyrQfJRAQGQHM9ZKiDdYx1AR":
                lines[0] = "SunSUN_TRXPool"
            elif lines[1] == "TDB8Y2WMMeRivgxdsYniAyrGNWdCQisCvQ":
                lines[0] = "SunJST_TRXPool"
            elif lines[1] == "TWPcaMKwJAqHk7Ta3fYdHaHeBU2kES9TLH":
                lines[0] = "SunWBTT_TRXPool"
            elif lines[1] == "TLCWfcYqmYZ6anvfq8AVPSiUuvRKwTyQx5":
                lines[0] = "SunBTC_TRXPool"
            elif lines[1] == "TWnTQ5grjn4nAJThs4JVGcyCYzzACd4ycq":
                lines[0] = "SunUSDT_TRXPool"
            elif lines[1] == "TLNBj6KNXMxcQutEPjgqotA6Wvr5mEVNd6":
                lines[0] = "SunUSDJ_TRXPool"
            elif lines[1] == "TGTN3wq6bDNMxvzYZrJqq6irJ9M1HWYAxX":
                lines[0] = "SunWIN_TRXPool"
            elif lines[1] == "TWKrCJCaeMzvixk8y1QLNbfwNVEjZz3CYF":
                lines[0] = "SunETH_TRXPool"
            elif lines[1] == "TNRd6HfeWosrZKe3J1eFbwXS57M71wH5K2":
                lines[0] = "BTCST-TRX"
            st += "\t".join(lines)
        fw.write(st)

def main():
    startBlock = "28473800"
    endBlock = "28584835"
    fileNameList = getFileName(startBlock,endBlock)
    parse(fileNameList)

if __name__ == '__main__':
    main()