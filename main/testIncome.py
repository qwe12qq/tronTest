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
# }

def calcu(tokenDict,tokenAddressDict,farmDict,blockNumDict,speedict):
    token_count_dict1,token_count_dict2 ={},{}
    dec = 1000000000000000000000000000000000000
    dec18 = 1000000000000000000

    for address,info_list in tokenAddressDict.items():
        result = 0
        for ele in info_list:
            account_address = ele["address_address"]
            accrued = int(ele["accrued"])
            farm_index = int(ele["farm_index"])
            balance = int(ele["balance"])
            curr_index1 = int(tokenDict[address])
            # index_del1 = float(curr_index1) - float(farm_index)
            # curr_index2 = farmDict[token_address]

            index_del2 = float(curr_index1) - float(farm_index)

            # if  index_del1 <= 0 :
            #     index_del1 = 0
            if  index_del2 <= 0 :
                index_del2 = 0
            # res1 = index_del1 * balance / dec + accrued
            res2 = index_del2 * balance / dec + accrued
            result+=res2
            # if token_address not in token_count_dict1.keys():
            #     token_count_dict1[token_address] = res1
            # else:
            #     token_count_dict1[token_address] += res1
            # if token_address not in token_count_dict2.keys():
            #     token_count_dict2[token_address] = res2
            # else:
            #     token_count_dict2[token_address] += res2
    # print (token_count_dict1)
        print (address,result)
        token_count_dict2[address] =result
        result2 = (blockNumDict[address]-25667132)*speedict[address]*dec18/(3600*24/3-6)
        result3 = (blockNumDict[address]-25667132)*speedict[address]*dec18/3600/24*3
        print (address,result,result2,result3,result2-result,result3-result)
    # print (token_count_dict2)
    return token_count_dict2

#获取token 对应的farmindex
#id,address,total_balance,block_number,farm_index,farm_speed,create_time,update_time
def parsedict(ft):
    resDict = {}
    speendDdict = {}
    blockNumdict = {}
    farm_dict ={}
    for ele in ft:
        if "address" in ele :
            continue
        else:
            l = ele.split(",")
            resDict[l[1]] = l[4]
            speendDdict[l[1]] = float(l[5])
            blockNumdict[l[1]] = int(l[3])
            blnum = 25667132
            speed = float(l[5]) * 1000000000000000000 / (3600*24/3-6)
            delbl = blnum - int(l[3])
            acc = speed * delbl
            ratio = float(acc) * 1000000000000000000000000000000000000 / float(l[2])
            fi = float(l[4]) + ratio
            farm_dict[l[1]] = fi

    return resDict,speendDdict,blockNumdict,farm_dict

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
            if l[2] not in resdict.keys():
                resdict[l[2]] = []
            resdict[l[2]].append({"address_address":l[1],"balance":l[3],"farm_index":l[4],"accrued":l[6]})
    f = open("res1","w")
    f.write(str(resdict))
    return resdict

#speed/24/3600*3*num  应该发送多少
def getRes(res1,res2,speedDict,blockNumDict1,blockNumDict2):
    for jtoken,val in res1.items():
        cz = val - res2.get(jtoken,0)    #实际发放的
        # num = blockNumDict2[jtoken] - blockNumDict1[jtoken]
        num = blockNumDict2[jtoken] - 25667132
        # print (jtoken,speedDict[jtoken],num)
        distribution = speedDict[jtoken]*1000000000000000000*3*num/24/3600
        print (jtoken,"实际：",cz,"应该：",distribution,"差值：",cz-distribution)

def main():
    ft1 = open("../data/account_status3.csv","r").readlines()
    fttoken1 = open("../data/token_status3.csv","r").readlines()
    ft2 = open("../data/account_status.csv","r").readlines()
    fttoken2 = open("../data/token_status.csv","r").readlines()

    # token_fmindex_dict1,token_speed_dict,blockNumDict1,farmDict1 = parsedict(fttoken1)
    # address_dict1 = parse2(ft1)
    # res1 =  calcu(token_fmindex_dict1,address_dict1,farmDict1)

    token_fmindex_dict2,speedict2,blockNumDict2,farmDict2 = parsedict(fttoken2)
    address_dict2 = parse2(ft2)
    res2 =  calcu(token_fmindex_dict2,address_dict2,farmDict2,blockNumDict2,speedict2)
    # getRes(res2,{},speedict2,blockNumDict2,blockNumDict2)

if __name__=="__main__":
    main()