import os, sys
import json
import redis

def main():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('name', 'hello')
    print(r.get("name"))
    # 批量设置值
    r.mset({"name1":'zhangsanq', "name2":'lisqi'})
    r.append('namwwwe1', 'OK')
    li=["name1","name2"]
    print(r.mget(li),r.get("namwwwe1"))

if __name__ == '__main__':
    main()
