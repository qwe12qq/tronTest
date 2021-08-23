import os,sys

def calcu(tokenAddressDict,tokenDict,tokenBlockNumber,speed):
    startNumver=25667132
    dec36 = 1000000000000000000000000000000000000
    dec18 = 1000000000000000000
    f = open("res","w")
    f.write(str(tokenAddressDict))
    for address,info_list in tokenAddressDict.items():
        result=0
        curr_index1 = int(tokenDict[address])
        for ele in info_list:
            accrued = int(ele["accrued"])
            farm_index = int(ele["farm_index"])
            balance = int(ele["balance"])

            index_del1 = curr_index1 - farm_index
            if  index_del1 < 0 :
                index_del1 = 0
            res1 = index_del1 * balance / dec36 + accrued

            result += res1
        # print (address,result)
        result2 = (tokenBlockNumber[address]-startNumver)*speed[address]*dec18/(3600*24/3-6)
        print (address,result,result2)
        print (result2-result)
    return

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
            speendDdict[l[1]] = int(l[5])
            blockNumdict[l[1]] = int(l[3])
            blnum = 25748749
            speed = int(l[5]) * 1000000000000000000 / (3600*24/3)
            delbl = blnum - int(l[3])
            acc = speed * delbl
            ratio = int(acc) * 1000000000000000000000000000000000000 / float(l[2])
            fi = int(l[4]) + ratio
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
            resdict[l[2]].append({"account_address":l[1],"balance":l[3],"farm_index":l[4],"accrued":l[6]})

    return resdict

def main():
    ft1 = open("../data/account_status.csv","r").readlines()
    fttoken1 = open("../data/token_status.csv","r").readlines()

    address_dict1 = parse2(ft1)
    token_fmindex_dict1,token_speed_dict,blockNumDict1,farmDict1 = parsedict(fttoken1)
    calcu(address_dict1,token_fmindex_dict1,blockNumDict1,token_speed_dict)

if __name__=="__main__":
    main()