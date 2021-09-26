import pymysql


'''
This document includes basic interactive operations of mysql database
author: yunly.liu
'''

class mysqlOperate:
    def __init__(self,host,port,user,pw,db):
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.db = db
        self.cursor = ''


    def connect(self):
        connection = pymysql.connect(host=  self.host,port = self.port,
                             user = self.user,password = self.pw,db = self.db,charset='utf8')
        # 使用cursor()方法获取操作游标
        self.cursor = connection.cursor()

    def selectMysql(self,sql):
        list = []
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            list = results   #return is list type
        except:
            print ("Error: mysql unable to select data")
        return list

    def close(self):
        self.cursor.close()

if __name__ == '__main__':
    host = "123.56.166.152"
    port = 3306
    user = "defi"
    pw = "wEJdXe3LIsClKpk6"
    db = "defi-swapqa"

    op = mysqlOperate(host,port,user,pw,db)
    op.connect()
    sql = 'select * from `swap_liquidity_user` where user_address = "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS";'
    l = op.selectMysql(sql)
    print (l)
