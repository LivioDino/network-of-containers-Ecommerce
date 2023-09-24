#!/usr/bin/env python3

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

redis_host = "redis"
stream_key = "skey"
stream2_key = "s2key"
group1 = "grp1"
group2 = "grp2"

import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import asyncio
from postgrest import AsyncPostgrestClient

'''
METHODS FOR COMMUNICATION CLIENTE-SIDE
'''

# old method
def getEntryData(l): 

        entryData=[]
        # Get data from read entries
        print("Get data from new messages")
        first_stream = l[0]
        print( f"got data from stream: {first_stream[0]}")
        fs_data = first_stream[1]
        # print(fs_data)
        dict={}
        for id, value in fs_data:
            
            print( f"id: {id} eventType: {value[b'eventType']} value: {value[b'amount']} item_id: {value[b'item_id']}")
            # r.xdel(stream_key, id)
        dict["id"]=id
        entryData.append(dict)
        print(entryData)
        return entryData

# new method
def getEntryData2(l):
    print("-- getting entry data --")
    [[stream, [[id, values]]]] = l
    diz=dict(values)
    diz["id"]=id
    return diz

def delMessages():
    print("-- deleting all ids entries from the stream -- \n")

    s1 = r.xread( streams={stream_key:0} )
    for streams in s1:
        stream_name, messages = streams

    [ r.xdel( stream_name, i[0] ) for i in messages ]

def readStream():

    print( f"stream length: {r.xlen( stream_key )}")
    print("-- waiting 10 sec for new messages on stream")

    # wait for 10s for new messages
    l = r.xread( count=5, block=10000, streams={stream_key: '$'} )
    print( f"stream length: {r.xlen( stream_key )}")
    print( f"after 10 sec block, got {l} new messages on the stream \n")

    return l

def writeACKStream2(ack):
    
    print( f"stream length before write: {r.xlen( stream2_key )}")
    print("-- writing on stream2")
    r.xadd(stream2_key, ack)

    print( f"stream length after write: {r.xlen( stream2_key )} \n")

'''
METHODS FOR COMMUNICATING DB-API-SIDE
'''

async def selectall():
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        r = await client.schema("api").from_("ogginvendita").select("*").execute()
        return r   
    
# async def selectall():
#     async with AsyncPostgrestClient("http://localhost:3000") as client:
#         r= await client.from_("countries").update({"capital": "Hà Nội"}).eq("name", "Việt Nam").execute()
#         return r   

'''
BEGIN OF MAIN
'''

# connect to redis
r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# del all ids entries from the stream
if (r.xlen( stream_key )): # id l not empty
    delMessages()

print("ServerCliente starting!\n")

while True:

    ll = readStream()

    if (ll): # id l not empty

        # get data
        messageDiz=getEntryData2(ll)
        print(messageDiz, "\n")

        print("checking eventType")

        ack={"idRefToOrig": messageDiz.get("id"), "error": "False"}
        if messageDiz["eventType"]=="itemlist":

            # richiedi snapshot db (check eventuali condizioni)
            temp = asyncio.run(selectall())
            snap=temp.data
            print(snap)

            # ack = append lista/diz di oggetti dal db

            # ack "error" = True se ci sono errori
            # manda ack a cliente

        elif messageDiz["eventType"]=="purchase":
            # richiedi db di aggiungi ogg in tabella diversa e aggiusta quantità
            
            # ack "error" = True se ci sono errori
            # manda ack a cliente
            pass

        else:
            print("ERRORE eventType NON DEFINITO")


        # # sleep time simualtes requirements computation
        # print("-- sleep time simualtes requirements computation\n")
        # time.sleep(2)

        print("-- creating ack and sending to cliente\n")
        # creating ack and sending to cliente
        
        
        writeACKStream2(ack)
        writeACKStream2(snap)
        





# redis_client = redis.StrictRedis("0.0.0.0", decode_responses=True)
# response = redis_client.xread({'mystream': "$"}, count=1, block=50000)
# if len(response) > 0:
#     min_value = response[0][1][0][0] # [['mystream', [('1596618943439-0', {'mykey': 'myval'})]]]
#     time.sleep(50) # wait for the end of the window
#     entries = redis_client.xrevrange('mystream', max="+", min=min_value, count=5)

    




