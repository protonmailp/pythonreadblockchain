import requests
import json
import time
from requests.auth import HTTPBasicAuth
from elasticsearch5 import Elasticsearch
from elasticsearch5 import helpers

es = Elasticsearch()
blockhashs=[]
txids=[]
def getblockhash(height,step):
    url = "http://127.0.0.1:8332"
    commands = [{"method":"getblockhash","params":[h],"id":"jsonrpc" } for h in range(height, height + step)]
    r = requests.post(url, data=json.dumps(commands), auth=("admin", "admin"), headers={'content-type': "application/json"})
    jblockhash =json.loads(r.content.decode("utf-8"))
 #   print(jblockhash)
    for jb in jblockhash:
        blockhashs.append(jb["result"])
 #       print(jb['result'])
 #   print(blockhashs)


def getblock(height,step):
    url = "http://127.0.0.1:8332"


    blockhashs1=blockhashs[height:(height + step)]
    commands = [{"method": "getblock", "params": [blockhash], "id": "jsonrpc"} for blockhash in blockhashs1]

    r = requests.post(url, data=json.dumps(commands), auth=("admin", "admin"), headers={'content-type': "application/json"})
    jblock =json.loads(r.content.decode("utf-8"))
    for block in jblock:
        txs =block['result']['tx']
#        print(txs)
        for tx in txs:
            txids.append(tx)


def getrawtransaction():
    url = "http://127.0.0.1:8332"
    j=0
    while True:

        if j<=len(txids)-1000:
            txids1 =txids[j:(j+1000)]
            commands = [{"method": "getrawtransaction", "params": [txid,1], "id": "jsonrpc"} for txid in txids1]
            r = requests.post(url, data=json.dumps(commands), auth=("admin", "admin"),headers={'content-type': "application/json"})
            jrawtransaction = json.loads(r.content.decode("utf-8"))
            toelastic=[]
            for i in range(1000):
                vinstringarray = []
                voutstringarray = []
                vins = jrawtransaction[i]['result']['vin']
                vouts = jrawtransaction[i]['result']['vout']
                for vin in vins:
                    if 'coinbase' not in vin:
                       # print(vin)
                        vinstringarray.append(vin['txid']+str(vin['vout']))

                for vout in vouts:
                    if vout['scriptPubKey']['type']  in ["pubkey","pubkeyhash"]:
                        try:
                            voutstringarray.append(vout['scriptPubKey']['addresses'][0])
                        except:
                            print(vout)
                            pass

                doc = {
                    '_op_type': 'index',
                    '_index': 'btc',
                    '_type': 'info',
                    '_id': txids1[i],
                    "_source": {
                        "i": ",".join(vinstringarray),
                        "o": ",".join(voutstringarray)
                    }
                }
                toelastic.append(doc)
            helpers.bulk(es, toelastic)

        elif j<len(txids) and j!=len(txids) :
            txids1 =txids[j:len(txids)]
            commands = [{"method": "getrawtransaction", "params": [txid,1], "id": "jsonrpc"} for txid in txids1]
            r = requests.post(url, data=json.dumps(commands), auth=("admin", "admin"),headers={'content-type': "application/json"})
            jrawtransaction = json.loads(r.content.decode("utf-8"))
            toelastic=[]
            for i in range(len(jrawtransaction)):
                vinstringarray = []
                voutstringarray = []
                vins = jrawtransaction[i]['result']['vin']
                vouts = jrawtransaction[i]['result']['vout']
                for vin in vins:
                    if 'coinbase' not in vin:
                       # print(vin)
                        vinstringarray.append(vin['txid']+str(vin['vout']))

                for vout in vouts:
                    if vout['scriptPubKey']['type']  in ["pubkey","pubkeyhash"]:
                        try:
                            voutstringarray.append(vout['scriptPubKey']['addresses'][0])
                        except:
                            print(vout)
                            pass

                doc = {
                    '_op_type': 'index',
                    '_index': 'btc',
                    '_type': 'info',
                    '_id': txids1[i],
                    "_source": {
                        "i": ",".join(vinstringarray),
                        "o": ",".join(voutstringarray)
                    }
                }
                toelastic.append(doc)
            helpers.bulk(es, toelastic)


        else:
            print(str(j))
          #  print(txids[j])
            break
        j=j+1000
        print(str(j))


def gettotalblocks():
    url = "http://127.0.0.1:8332"
    command ={"method":"getinfo","params":[],"id":"jsonrpc"}
    r = requests.post(url, data=json.dumps(command), auth=("admin", "admin"), headers={'content-type': "application/json"})
    jinfo =json.loads(r.content.decode("utf-8"))
    return jinfo['result']["blocks"]


totalblocks =0
totalblocks =gettotalblocks()

print(totalblocks)

for i in range(1,totalblocks,1000):
    if totalblocks-i>=1000 :
        getblockhash(i,1000)
    elif totalblocks-i<1000 and totalblocks-i>0:
        getblockhash(i,totalblocks-i)
    else:
        pass

for i in range(502000,totalblocks,1000):
    print(i)

    if totalblocks-i>=1000:
        getblock(i,1000)
    elif totalblocks-i<1000 and totalblocks-i>0:
        getblock(i,totalblocks-i)
    else:
        pass

getrawtransaction()
newtotalblocks=0

while True:
    time.sleep(60)
    txids = []
    newtotalblocks = gettotalblocks()
    print(totalblocks)
    print(newtotalblocks)
    for i in range(totalblocks,newtotalblocks,1000):
        if newtotalblocks-i>=1000 :
            getblockhash(i,1000)
        elif newtotalblocks-i<1000 and newtotalblocks-i>0:
            getblockhash(i,newtotalblocks-i)
        else:
            pass

    for i in range(totalblocks,newtotalblocks,1000):
        if newtotalblocks-i>=1000 :
            getblock(i,1000)
        elif newtotalblocks-i<1000 and newtotalblocks-i>0:
            getblock(i,newtotalblocks-i)
        else:
            pass

    getrawtransaction()
    totalblocks=newtotalblocks
    print("while ok")





# for i in range(1,502500,500): #1,500000
#     print("getblockhash")
#     print(i)
#     getblockhash(i)
# for i in range(299001,400000,500):  # 1 200000 , 1900000 300000 , 299001 400000,
#     print("getblock 1")
#     print(i)
#     getblock(i)
#
# print(len(txids))
# getrawtransaction()

# txids =[]
# for i in range(399501,460000,500):  # 1 200000 , 1900000 300000 , 299001 400000,
#     print("getblock 2")
#     print(i)
#     getblock(i)
#
# print(len(txids))
# getrawtransaction()


# txids =[]
# for i in range(459501,502500,500):  # 1 200000 , 1900000 300000 , 299001 400000,
#     print("getblock 3")
#     print(i)
#     getblock(i)
#
# print(len(txids))
# getrawtransaction()



#6a41a9e289682837f4a5dca6fd79c62eaa50c592842cd0f89546e56b652b8540 1,200000

# data={"method":"getinfo","params":[],"id":"jsonrpc"}
# a=[]
# a.append(data)
# a.append(data)
#
#
#
# r=requests.post(url,data=json.dumps(a), auth=("admin", "admin"),headers={'content-type':"application/json"})
# print(r.status_code)
# print(r.headers)
# print(r.content.decode("utf-8"))
# jh=json.loads(r.content.decode("utf-8"))
# try:
#     print(jh[1]["result"]["blockss"])
# except KeyError:
#     print("chu cuo le")


# import redis
# r = redis.Redis(host='localhost', port=6379, db=0)

# with r.pipeline() as pipe:
#     pipe.multi()
#     for i in range(100):
#         pipe.lpush("a",i)
#     pipe.execute()
# a=[]
# with r.pipeline() as pipe:
#     pipe.multi()
#     for i in range(100):
#         pipe.rpop("a")
#     a=pipe.execute()
#
# a=a.
# print(a)

