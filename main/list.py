import os,sys
import requests
import json

def main():
    url_wb = "https://testapi.justswap.io/swap/v2/exchanges/default"
    url_all = "https://testapi.justswap.io/swap/v2/exchanges"
    res = requests.get(url_all).text
    res_wb = requests.get(url_wb).text

    all_list,w_list,b_list=[],[],[]

    for ele in json.loads(res)["data"]["body"]:
        all_list.append(ele["tokenAddress"])

    for e in json.loads(res_wb)["data"]["white"]:
        w_list.append(e["tokenAddress"])
    for e in json.loads(res_wb)["data"]["black"]:
        b_list.append(e["tokenAddress"])

    print (len(list(set(all_list).difference(set(w_list)))))
    print (len(list(set(all_list).difference(set(b_list)))))
    print ((list(set(all_list).difference(set(b_list)))))

if __name__=="__main__":
    main()