#!/usr/bin/env python3

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

redis_host = "redis"
stream_key = "skey"
stream2_key = "s2key"
group1 = "grp1"
group2 = "grp2"
sleeptime = 4

import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import uuid

def connectToRedis():
    rr = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    return rr

def readACKStream2(stream2_key):
     
    print( f"stream length: {r.xlen( stream2_key )}")
    print("-- waiting 10 sec for new messages on stream2")

    # wait for 10s for new message
    ll = r.xread( count=5, block=10000, streams={stream2_key: '$'} )
    print( f"stream length: {r.xlen( stream2_key )}")
    print( f"after 10 sec block, got {ll} new messages on the stream2 \n")
    return ll

def getEntryData2(ll):
    print("-- getting entry data --")
    [[stream, [[id, values]]]] = ll
    diz=dict(values)
    diz["id"]=id
    return diz

def writeStream(stream_key, event):
    
    print( f"stream length before write: {r.xlen( stream_key )}")
    print("-- writing on stream2")
    r.xadd(stream_key, event)
    print( f"stream length after write: {r.xlen( stream_key )} \n")

def requestItemList():
    # genra evento Itemlist e manda su stream
    event = {"eventType": "itemlist", "condition":""}
    writeStream(stream_key, event)

    # aspetta ack su stream 2
    l = readACKStream2(stream2_key)
    if (l): # id l not empty
        messageDiz=getEntryData2(l)
        print(messageDiz, "\n")

    # ritorna messageDiz (Chew sarebbe ListDiz)    
    return messageDiz
    

def requestPurchase(DizOgg):
    # evento da definire dopo aver ricevito ItemList
    event = {"eventType": "purchase"}
    event.update(DizOgg)
    writeStream(stream_key, event)

    # aspetta ack su stream 2
    l = readACKStream2(stream2_key)
    if (l): # id l not empty
        messageDiz=getEntryData2(l)
        print(messageDiz, "\n")

def createStreams():
    # genero id unico (usa indirizzo mac + timestamp)
    uniqueid = str(uuid.uuid1())
    print ("The random id using uuid1() is :", uniqueid)

    # crea nuova stream di output (skey) e input (skey2)
    
    skey = uniqueid + "input"
    skey2 = uniqueid + "output"
    print ("creo 2 nuove streams", skey, skey2)
    entryTest= {"test":0}
    writeStream(skey, entryTest)
    writeStream(skey2, entryTest)
    r.xdel( skey, 1 )
    r.xdel( skey2, 1 )
    print("len delle stream(deve essere 00):", r.xlen(skey), r.xlen(skey2))

if __name__ == '__main__':
    '''
    BEGIN OF MAIN
    '''

# events are requests made by client io order to buy something
# old event = {"eventType": "purchase", "amount": 5, "item_id": "XXX"}

# first entry is eventType (itemlist/purchase), next entries are (objID:quantity)
event = {"eventType": "itemlist", "18312": 5, "11023" :2}


# # --- temp cicle simulation of different clients sending
# while True:

#     print( f"stream length before write: {r.xlen( stream_key )}")  

#     #Code for writing a stream directly:
#     print("-- writing on stream")
#     r.xadd(stream_key, event)

#     print( f"stream length after write: {r.xlen( stream_key )}")

#     print("sleep for", sleeptime, "sec \n")
#     time.sleep(sleeptime)


# --- single send and ack read (real client scenario)
r = connectToRedis()
createStreams()
writeStream(stream_key, event)

l = readACKStream2(stream2_key)

if (l): # id l not empty
    messageDiz=getEntryData2(l)
    print(messageDiz, "\n")