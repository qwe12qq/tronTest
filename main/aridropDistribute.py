import os, sys
import json

'''
空投验证3个维度：
1. 本期新增加黑名单数量
2. 原始的数据校验
3. 本期即将空投数据总和
'''
def main2():

#0x0E636D680B300214CF10E3343D0EEF14F642C8A4 是白名单
    # white = ["0x9f5ea6af1ce2e330c369b67bf31bdccc1e9a1123","0x9e390b073aa35c4ffc893791a5670fca36190b6f","0x6544df975cf58a0b2c9a361a8db2e00d338e10c1","0x519b6d47a5ae8eb6ef3817f126d796a25b034dfe","0x86587327a9dbea6ef2d4fbc142be241801b858b2","0x11598f24ff51be40891fd48555478e725071c683","0xdce75e914cb8b427ecc032b6edf1e9a249097852","0xa426ba758dbe238ea8811b786856f2d9d88efaad","0x04153776761994d676c68147b89f9bdffbaef512","0xafea5b52c980bda1c5bd43dcb381a1b295213e77","0xd3adfeda41e7756151741fcb5f763f461bc4304f","0x4863c245d76bf89461f8855917b45c45c4bd5293","0xcbf7a0d2107aaab905e44c0b980accd9b348836d","0x43a3a118cd0980f8acfd6cee25bee61d314d6da3","0xd5102725cc00421854dd616a2d8769ce36017315","0x62eabbfe4a558051c473fe339a599d9e1bae9434","0x7d7032134d6aafeb1564720917150ff89fafce9d","0xbd11ff906bcb72c2df54cbc6ec29a8192f15782a","0x5278223b78ce6a50cd0e5e237104c4ef65760f65","0x22543defc522e22150f0915f51419e9dda58b474","0xcd87b3c827184f09a8e0b0d4f5eeca9c4eb6fcc0","0x12158ec38b398631fbed34a8faedb988527e5323","0x5275817b74021e97c980e95ede6bbac0d0d6f3a2","0x84b81987f6ca3cde2a50daca42a58a132099c731","0x10f789f11e90e67438066431fb5d0943f7847ea8","0x49de76e8e7c1b6a974d6b766b9b5f5d199566e94","0xc7048830a7b0d67d712ffd59f879a9b8b1f48a4a","0xc5aa216ab58291b7cfe9be87c0e46917de032907","0x49244549548015494659e77e4f819186401fc2ad","0x74543949fe2ca01a1cdef9209b178626262a943b","0x3cddcb8cf10c4facfbf960309806d8a3a3f19a40","0xb943e534ccb68a976bfa9007ad6705c76da81ec6","0x05c69e40ed489b88fd694ad7e31776e469859afd","0x475021e2cbfe925beafb63084646eaa8ffe195e7","0xa29f76f2c2a57bd8c1fc865543d800a093f34e3f","0xc00c892d97e318bca7592f5dcd462df8d36bb3fd","0xab0922c53e751abfc39121a54e9352f56f8bb5c1","0xe1acc251656c2964678a8843808dfc2bdf56da20","0xe53085d26544daf3ba8f66b2d1b108e285cc51f9","0xc0513edb8acf4b0f42cb9ab92b2b667717e33636","0xd3b1582c1f8df3f3c054ce18393fd68df5e2d756","0xe81ef15f525c82e49d6df6d113b5fac35fa8c559","0x453fc0de99708a1761e6fe69f77ca7356892b64e","0x76d2ddce6b781e66c4b184c82fbf4f94346cfb0d","0x68b4683475747e28a83596e94b58187d452099cf","0x008de4b238bc4507c6e11ce875ae45878c08d0e9","0x4fadd86fcadb8dca5e8963983c2a6e0c6f61a18f","0x0c0057af75d6fcb35566621e8639ba06755c4c29","0x29f82d09c2afd12f3c10ee49cd713331f4a7228e","0xafab1adfb25e919d9f6ee7196f1ad0ffa93cad12","0xa1cb4468f529f51296180d148f4764adde8563a3","0xa61b636d74df04d364c3c508ac74c3af928a64d2","0xf9acfe81062a1c1bc07b7f88de4aa44dff13d0e0","0x86d8201702fc3cd023eec0f59d4a416b547dcdb6","0x1ae6912e08bb3e105a4f0a60f666376d3c7af380","0x6119fa6c5b18be03f3b8e408c961e28239a0108c","0x5e95149b4c377adc3d29786ac2dec57a58f38a5d","0xb4baeb9b6591c9b842e5af3e7b3b30c4e6e42cfa","0x3c739ec88a51793101cd59313b85415d8d01ee7f","0x62b3c674d198b490d81c39f573734c580a8aeecd","0x6d1105ba1b4effb4073e99df2c8ff17ebffff0a8","0x60cc8e2642781c0575e81fd53bb7c6d2829ff423","0x02187e006a37641f4b694cabb713204d20f8c6be","0x41ce0fe7cd60b23b78c24126f122f72686247395","0xca14697a2799573915884ff7860ba1c452a46fbf","0xe4f36a7e86148956ce733a03c61903bb44af1deb","0x5102009e110466f69c1e82d0c64ef969339648d4","0xed44745042ffbc012b19788ed78f8d539cd12c02","0xfe8fc68127e2a40f477aa406da0da3ec5a2f5a43","0xb8c7fca90863d00e033f749b81ab816608f9ef37","0x66d82cc14cd3115c3ca30a0d716863e720f4b555"]
    white = ['0x0e636d680b300214cf10e3343d0eef14f642c8a4','0xafea5b52c980bda1c5bd43dcb381a1b295213e77', '0x7d7032134d6aafeb1564720917150ff89fafce9d', '0xfe8fc68127e2a40f477aa406da0da3ec5a2f5a43', '0xafab1adfb25e919d9f6ee7196f1ad0ffa93cad12', '0x29f82d09c2afd12f3c10ee49cd713331f4a7228e', '0x84b81987f6ca3cde2a50daca42a58a132099c731', '0x008de4b238bc4507c6e11ce875ae45878c08d0e9', '0x3dfbc47e76171a82a5121ada179c73d00b60ba22', '0xc7048830a7b0d67d712ffd59f879a9b8b1f48a4a', '0x62eabbfe4a558051c473fe339a599d9e1bae9434', '0xca14697a2799573915884ff7860ba1c452a46fbf', '0x41ce0fe7cd60b23b78c24126f122f72686247395', '0xb8c7fca90863d00e033f749b81ab816608f9ef37', '0xd3adfeda41e7756151741fcb5f763f461bc4304f', '0x6119fa6c5b18be03f3b8e408c961e28239a0108c'];
    accountList02,accountList09,accountList16,accountList23 = [],[],[],[]
    fblc = open("../data/not_active_account_blacklist-2021-09-22.json",'r').read()
    f09 = open("../data/distribution-2021-09-01.json", 'r').read()
    f23 = open("../data/distribution-2021-08-25.json", 'r').read()
    f16 = open("../data/distribution-2021-09-08.json", 'r').read()
    f02 = open("../data/distribution-2021-09-15.json", 'r').read()
    c09, c23, c16, c02 = json.loads(f09), json.loads(f23), json.loads(f16), json.loads(f02)
    fb = eval(fblc)
    for cont in c02["claims"]:
        if cont not in accountList02 and cont not in white:
            accountList02.append(cont)
    for cont in c09["claims"]:
        if cont not in accountList09 and cont not in white:
            accountList09.append(cont)
    for cont in c16["claims"]:
        if cont not in accountList16 and cont not in white:
            accountList16.append(cont)
    for cont in c23["claims"]:
        if cont not in accountList23 and cont not in white:
            accountList23.append(cont)
    # print()
    tmp = list(set(accountList23).intersection(set(accountList16)))
    tmp = list(set(tmp).intersection(set(accountList09)))
    tmp = list(set(tmp).intersection(set(accountList02)))
    # print(list(set(tmp).difference(set(fb))))
    assert list(set(tmp).difference(set(fb))) == [],"本期新增加的黑名单不一致"
    print("本期黑名单数量：",len(tmp))

    return tmp

def main():
    blackList = main2()
    airlst = []
    endlst = []
    amountend = 0
    f = open("../data/origin-distribution-2021-09-22.json", 'r').read()
    fbal = open("../data/balances-2021-09-22.json", 'r').read()
    fend = open("../data/distribution-2021-09-22.json", 'r').read()
    cend = json.loads(fend)
    # print("content end length:",len(cend["claims"]))
    for act,ele in cend["claims"].items():
        endlst.append(act)
        jsonele = int(ele["amount"], 16)
        amountend += jsonele
    print("本次发放总数值：",amountend/1e18)

    content = json.loads(f)
    bals = json.loads(fbal)
    totalsupplyEth = 0

    total = int(content["tokenTotal"], 16)
    claims = content["claims"]
    print("源数据账户数量：", len(claims))
    amount = 0

    for acc, val in bals.items():
        totalsupplyEth += int(val)
    print("源数据totalsupply:", totalsupplyEth)

    for account, ele in claims.items():
        if account not in blackList:
            # fair.write(account+"\n")
            airlst.append(account)
        calele = int(bals.get(account)) / totalsupplyEth * 3827063 * 1e18
        jsonele = int(ele["amount"], 16)
        assert calele - jsonele < 1e10, "账户：%s,计算：%s,json文件：%s,差值：%s" % (account, calele, jsonele, calele - jsonele)
        amount += jsonele


    print("源数据发放数量：",amount, total)
    assert total - 3827063 * 1e18 == 0, "total is not equal amount!"
    assert amount == total, "total is not equal amount!"
    # print(len(list(set(airlst).difference(set(endlst)))))

if __name__ == '__main__':
    main()

