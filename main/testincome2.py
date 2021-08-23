import os,sys
# demo
# public class FarmGainDTO {
#     String balance;
#     Long blockNumber;
#     String accrued;
#     String farmIndex;
#     public String getCurrentGain(String currIndex) {
#     BigInteger indexDelta = new BigInteger(currIndex).subtract(new BigInteger(farmIndex));
#     if (indexDelta.compareTo(BigInteger.ZERO) < 0) {
#         indexDelta = BigInteger.ZERO;
#     }
#     return indexDelta
#     .multiply(new BigInteger(balance)).divide(SolMath.WAD36).add(new BigInteger(accrued))
#     .toString();
#     }
# token 是token_status表数据
# blockNumber  当前高度 (快照的时候最大高度)
# speed = new BigInteger(token.getFarmSpeed()).multiply(BigInteger.TEN.pow(18)).divide(BigInteger.valueOf(3600 * 24 / 3));
# long deltaBlocks = blockNumber - token.getBlockNumber();
# BigInteger accrued = speed.multiply(BigInteger.valueOf(deltaBlocks));
# BigInteger ratio = accrued.multiply(BigInteger.TEN.pow(36)).divide(token.totalBalance);
# token.farmIndex = token.farmIndex.add(ratio);# }


def calcu(tokenDict,tokenAddressDict,farmDict,speedict2,blockNumDict2,totalbaldict,tokenfarmdaict2):
    token_count_dict1,token_count_dict2 ={},{}
    i=0
    all1,all2 = 0,0
    dec = 1000000000000000000000000000000000000
    dec18 = 1000000000000000000
    f22 = open("../data/airdrop-20210308.txt").readlines()
    f15 = open("../data/airdrop-20210301.txt").readlines()
    f = open("res","w")
    airdict,airdictold = {},{}
    for e in f22 :
        tmp = e.replace("\n","").split()
        airdict[tmp[1]] = tmp[-1]
        all1 += float(tmp[-1])
    for e in f15 :
        tmp = e.replace("\n","").split()
        airdictold[tmp[1]] = tmp[-1]
        all2 += float(tmp[-1])

    for address,info_list in tokenAddressDict.items():
        resAll = 0
        air = 0
        if address not in airdict:continue
        for ele in info_list:

            res1 ,result2= 0,0
            token_address = ele["token_address"]
            accrued_a = float(ele["accrued"])
            farm_index = int(ele["farm_index"])
            balance = float(ele["balance"])
            curr_index1 = int(tokenDict[token_address])
            curr_index2 = farmDict[token_address]
            index_del1 = float(curr_index2) - float(farm_index)
            # index_del2 = float(curr_index2) - float(farm_index)


            index_del2 = float(curr_index2) - float(farm_index)
            startNumber = 25667132
            endNumber = 28271791
            deltaBlocks = endNumber - blockNumDict2.get(token_address)

            # speed = new BigInteger(token.getFarmSpeed()).multiply(BigInteger.TEN.pow(18)).divide(BigInteger.valueOf(3600 * 24 / 3));
            # long deltaBlocks = blockNumber - token.getBlockNumber();
            # BigInteger accrued = speed.multiply(BigInteger.valueOf(deltaBlocks));
            # BigInteger ratio = accrued.multiply(BigInteger.TEN.pow(36)).divide(token.totalBalance);
            # token.farmIndex = token.farmIndex.add(ratio)
            speed = tokenfarmdaict2.get(token_address)*dec18/(3600*24/3)
            accrued = speed*deltaBlocks
            ratio = accrued*dec/totalbaldict.get(token_address)
            farmIndex = tokenfarmdaict2.get(token_address)+ratio
            # index_del1 = float(farmIndex) - float(farm_index)
            if  index_del1 <= 0 :
                index_del1 = 0
            if  index_del2 <= 0 :
                index_del2 = 0
            res1 = index_del1 * balance /dec  + accrued_a
            res2 = index_del2 * balance /dec + accrued_a

            if token_address not in token_count_dict1.keys():
                token_count_dict1[token_address] = res1
            else:
                token_count_dict1[token_address] += res1
            if token_address not in token_count_dict2.keys():
                token_count_dict2[token_address] = res2
            else:
                token_count_dict2[token_address] += res2
            # if token_address == "TR7BUFRQeq1w5jAZf1FKx85SHuX6PfMqsV":
            #     air = float(airdict.get(address,0)) - 150*dec18
            #     continue
            resAll += res1
            if resAll>float(airdictold.get(address,0)):
                resAll -= float(airdictold.get(address,0))
            air = int(airdict.get(address,0)) - int(airdictold.get(address,0))
            if air<0 :
                air = int(airdict.get(address,0))
        f.write(address+"\t计算应该发放： "+str(resAll) + "\t发放： "+str(air)+"\t计算-发放： "+str(resAll-air)+"\n")
    print ("now:",all1,"befor:",all2)
    return token_count_dict1
#获取token 对应的farmindex
#id,address,total_balance,block_number,farm_index,farm_speed,create_time,update_time
def parsedict(ft):
    resDict = {}
    speendDdict = {}
    blockNumdict = {}
    farm_dict ={}
    tokenfarmdaict = {}
    totalbaldict ={}
    for ele in ft:
        if "address" in ele :
            continue
        else:
            l = ele.split(",")
            resDict[l[1]] = l[4]
            speendDdict[l[1]] = float(l[5])
            blockNumdict[l[1]] = int(l[3])
            totalbaldict[l[1]] = int(l[2])
            tokenfarmdaict[l[1]] = int(l[4])
            blnum = 28271791
            speed = float(l[5]) * 1000000000000000000 / (3600*24/3)
            delbl = blnum - int(l[3])
            acc = speed * delbl
            ratio = float(acc) * 1000000000000000000000000000000000000 / float(l[2])
            fi = float(l[4]) + ratio
            farm_dict[l[1]] = fi
    return resDict,speendDdict,blockNumdict,farm_dict,totalbaldict,tokenfarmdaict
# id,address,token_address,balance,farm_index,block_number,accrued,create_time,update_time
def parse2(ft):
    resdict={}
    for ele in ft:
        if "address" in ele:
            continue
        else:
            l = ele.replace("\n","").split(",")
            # print (l)
            #账户address 维度分割
            if l[1] not in resdict.keys():
                resdict[l[1]] = []
            resdict[l[1]].append({"token_address":l[2],"balance":l[3],"farm_index":l[4],"accrued":l[6]})
    # f = open("res","w")
    # f.write(str(resdict))
    return resdict
#speed/24/3600*3*num  应该发送多少
def getRes(res1,res2,speedDict,blockNumDict1,blockNumDict2):
    for jtoken,val in res1.items():
        cz = val - res2.get(jtoken,0)    #实际发放的
        # num = blockNumDict2[jtoken] - blockNumDict1[jtoken]
        num = blockNumDict2[jtoken] - 25667132
        # print (jtoken,speedDict[jtoken],num)
        distribution = speedDict[jtoken]*1000000000000000000*3*num/24/3600
        print (jtoken,"实际：",cz,"应该：",distribution,cz-distribution)

def main():
    # ft1 = open("../data/account_status.csv","r").readlines()
    # fttoken1 = open("../data/token_status.csv","r").readlines()
    ft2 = open("../data/account (1).csv","r").readlines()
    fttoken2 = open("../data/token (1).csv","r").readlines()
    # token_fmindex_dict1,token_speed_dict,blockNumDict1,farmDict1 = parsedict(fttoken1)
    # address_dict1 = parse2(ft1)
    # res1 =  calcu(token_fmindex_dict1,address_dict1,farmDict1)
    token_fmindex_dict2,speedict2,blockNumDict2,farmDict2,totalbalancedict2,tokenfarmdaict2 = parsedict(fttoken2)
    address_dict2 = parse2(ft2)
    res2 =  calcu(token_fmindex_dict2,address_dict2,farmDict2,speedict2,blockNumDict2,totalbalancedict2,tokenfarmdaict2)
    # print(blockNumDict1,blockNumDict2)
    # getRes(res2,{},token_speed_dict,blockNumDict1,blockNumDict2)
if __name__=="__main__":
    main()