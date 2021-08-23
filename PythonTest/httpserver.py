import os,sys
from flask import Flask,request
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/demo',methods=['GET', 'POST'])
def hello_name():
    pg = request.args.get('p')
    p = int(pg)
    if (p > 60000000000000):
        return -1
    elif (p):
        str = {"page":p,2:{"h":1,"k":9},3:[2,1]}
    else:
        str = {"page":0,2:{"h":1,"k":9},3:[2,1]}
    return "{}".format(json.dumps(str))

@app.route('/test',methods=['GET', 'POST'])
def test():
    pg = request.args.get('p')
    res = hex(int(pg))
    return "{}".format(json.dumps(res))

if __name__ == '__main__':
    app.run()