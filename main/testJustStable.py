import os,sys
import requests
import json
import time
sys.path.append("..")
from PythonTest.operateMysql import *

class work():
    def __init__(self,cktime):
        self.db_dict = {}
        self.db_dictfeed = {}
        self.url_list = ["http://123.56.166.152:10088/scan/tokenInfo/timeLine/MKR",
                    "http://123.56.166.152:10088/scan/tokenInfo/timeLine/DAI",
                    "http://123.56.166.152:10088/scan/tokenInfo/timeLine/TRX",
                    "http://123.56.166.152:10088/scan/collInfo/timeLine"]
        self.urlfeed = "http://123.56.166.152:10088/scan/feedInfo/timeLine"
        self.tm = self.getTimeStr(cktime)

    def getDbData3kind(self,data):
        for row in data:
            self.db_dict = {"mkr_price":row[1],"mkr_supply":row[2],"dai_price":row[3],"dai_supply":row[4],
            "wtrx_lock":row[5],"ptrx_lock":row[6],"collateralization_ratio":row[7],
            "per_value":row[8],"trx_price":row[9],"trx_supply":row[10],"event_time":str(row[11])}

    def getDbData(self,data):
        for i in range(len(data)):
            evttm = self.getTimeStr(str(data[i][6]))
            exptm = self.getTimeStr(str(data[i][5]))
            self.db_dictfeed[evttm] = {"feed_price":data[i][4],"event_time":evttm,
                                "address":data[i][3],"expire_time":exptm}

    def getTimeStr(self,tm):
        timeArray = time.strptime(tm, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return  int(timestamp*1000)

    def getTmZoom(self,tm,period):
        startm = tm - period
        endtm = tm + period
        return startm,endtm

    def getHoursUrlRes(self):
        startm,endtm = self.getTmZoom(self.tm,300000)
        print("db_dict:",self.db_dict)
        for url in self.url_list:
            flag = url.split("/")[-1]
            flaglower = flag.lower()
            res = requests.get(url).text
            res = json.loads(res)
            assert res["code"]==0,"url ask failed！"
            for ele in res["data"]:
                if ele["t"] > startm and ele["t"] < endtm:
                    if flag in ["TRX","DAI","MKR"]:
                        price,supply = ele["price"],ele["supply"]
                        print("%s,price : %s, supply:%s"%(flaglower,price,supply))
                        assert price == self.db_dict[flaglower+"_price"] and \
                               supply == self.db_dict[flaglower+"_supply"],flag+" price or supply is not equal!"
                    else:
                        ptrxLocked,cRatio,per,wtrxLocked = \
                            ele["ptrxLocked"],ele["cRatio"],ele["per"],ele["wtrxLocked"]
                        assert ptrxLocked == self.db_dict["ptrx_lock"] and cRatio == self.db_dict["collateralization_ratio"] \
                        and per == self.db_dict["per_value"] and wtrxLocked == self.db_dict["wtrx_lock"] ,\
                        "collInfo/timeLine is error！"
                        print("ptrxLocked:%s,cRatio:%s,per:%s,wtrxLocked:%s"% (ptrxLocked,cRatio,per,wtrxLocked))

    def getFeedRes(self):
        startm,endtm = self.getTmZoom(self.tm,600000)
        res = requests.get(self.urlfeed).text
        res = json.loads(res)
        print ("db_dictfeed:",self.db_dictfeed)
        assert res["code"]==0,"url ask failed！"
        for ele in res["data"]:
            if ele["feedAddress"] != "TAbq6nbkWfzs5h2HvdQw2zb1cuFEwvhEny": continue
            for con in ele["feedEventDTOList"]:
                if con["lu"] > startm and con["lu"] < endtm:
                    address,price,lu,exp = con["address"],con["price"],con["lu"],con["exp"]
                    print("address:%s,price:%s,lu:%s,exp:%s"%(address,price,lu,exp))
                    assert address == "TAbq6nbkWfzs5h2HvdQw2zb1cuFEwvhEny","feed url address is error!"
                    assert price == self.db_dictfeed[lu]["feed_price"],"feed price is error!"
                    assert exp == self.db_dictfeed[lu]["expire_time"],"feed exp is error!"

def main():
    wk = work("2021-04-13 08:00:00")
    sthours = "2021-04-13 07:30:00"
    edhours = "2021-04-13 08:30:00"
    stfeed,edfeed = "2021-04-13 07:57:00","2021-04-13 08:10:00"
    host = "123.56.166.152"
    port = 3306
    user = "defi"
    pw = "wEJdXe3LIsClKpk6"
    db = "defi-qaversion120"
    cn = connectMysql(host,port,user,pw,db)
    sql = 'select * from t_tracker_hours ' \
          'where event_time>"{}" and event_time<"{}";'.format(sthours,edhours)
    l = selectMysql(cn,sql)
    wk.getDbData3kind(l)
    wk.getHoursUrlRes()

    sql = 'select * from t_feed_event ' \
          'where event_time>"{}" and event_time<"{}";'.format(stfeed,edfeed)
    l = selectMysql(cn,sql)
    wk.getDbData(l)
    wk.getFeedRes()
    close(cn)

if __name__ == '__main__':
    main()
