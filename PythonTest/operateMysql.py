import pymysql

def selectMysql(db,sql):
    list = []
    try:
        # 执行SQL语句
        db.execute(sql)
        # 获取所有记录列表
        results = db.fetchall()
        list = results
        # for row in results:
        #     fname = row[0]
        #     lname = row[1]
        #     age = row[2]
        #     sex = row[3]
        #     income = row[4]
        #     # 打印结果
        #     print ("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
        #            (fname, lname, age, sex, income ))
    except:
        print ("Error: unable to fetch data")

    # 关闭数据库连接
    return list

def close(db):
    db.close()

def connectMysql(host,port,user,pw,db):
    connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=pw,
                                 db=db,
                                 charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = connection.cursor()
    return cursor


if __name__ == '__main__':
    host = "123.56.166.152"
    port = 3306
    user = "defi"
    pw = "wEJdXe3LIsClKpk6"
    db = "defi-qaversion120"
    cn = connectMysql(host,port,user,pw,db)
    sql = "SELECT * FROM  t_tracker_hours limit 5;"
    l = selectMysql(cn,sql)
    print (l)
