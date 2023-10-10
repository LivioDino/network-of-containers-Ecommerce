#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import MYREDISconfig as cfg

REDIS_HOSTNAME=cfg.REDIS_HOSTNAME_S3
REDIS_PORT=cfg.REDIS_PORT_S3
REDIS_PASSWORD=cfg.REDIS_PASSWORD_S3

import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import asyncio
from postgrest import AsyncPostgrestClient

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
    diz["skeySIN"]=stream
    
    return diz

def getEntryData3(l):
    print("-- getting entry data --")
    listdiz=[]
    for i in l[0][1]:
        # print(i)
        # print(i[1])
        listdiz.append(i[1])

    return listdiz

def delMessages(stream_key):
    print("-- deleting all ids entries from the stream -- \n")

    s1 = r.xread( streams={stream_key:0} )
    for streams in s1:
        stream_name, messages = streams

    [ r.xdel( stream_name, i[0] ) for i in messages ]

def readStream(stream_key):

    print( f"stream length: {r.xlen( stream_key )}")
    print("-- reading from stream--")

    # ottieni lastid su hashmap con chiave "key"
    last_id_returned=r.hget("hashMapServerLastID", key)
    print("last_id_returned", last_id_returned)

    print( f"stream length: {r.xlen( stream_key )}")
    l = r.xread( count=100000, streams={stream_key: last_id_returned} )
    print(l)
    if (l): # il not empty
        # for id, value in l[0][1]:
        #     print( f"id: {id} value: {value[b'v']}")

        last_id_returned = l[0][1][-1][0]
        # salva lastid su hashmap con chiave "key"
        r.hset("hashMapServerLastID", key, last_id_returned)
        print( f"stream length: {r.xlen( stream_key )}")
    
    return l

def readStreamOneMess(stream_key):

    # print( f"stream length: {r.xlen( stream_key )}")
    # print("-- reading from stream--")

    # ottieni lastid su hashmap con chiave "key"
    last_id_returned=r.hget("hashMapServerLastID", key)
    # print("last_id_returned", last_id_returned)

    # print( f"stream length: {r.xlen( stream_key )}")
    l = r.xread( count=1, streams={stream_key: last_id_returned} )
    # print(l)
    if (l): # il not empty
        # for id, value in l[0][1]:
        #     print( f"id: {id} value: {value[b'v']}")

        last_id_returned = l[0][1][-1][0]
        # salva lastid su hashmap con chiave "key"
        r.hset("hashMapServerLastID", key, last_id_returned)
        print( f"stream length: {r.xlen( stream_key )}")
    
    return l

def readStreamOld(stream_key):
    
    global last_id_returned
    print("last_id_returned", last_id_returned)
    print( f"stream length: {r.xlen( stream_key )}")
    l = r.xread( count=1000, streams={stream_key: last_id_returned} )
    print(l)
    if (l): # il not empty
        # for id, value in l[0][1]:
        #     print( f"id: {id} value: {value[b'v']}")
        last_id_returned = l[0][1][-1][0]
        print( f"stream length: {r.xlen( stream_key )}")
    
    return l

def readStreamOldOld(stream_key):

    print( f"stream length: {r.xlen( stream_key )}")
    print("-- waiting 10 sec for new messages on stream")

    # wait for 10s for new messages
    l = r.xread( count=1000, block=10000, streams={stream_key: '$'} )
    print( f"stream length: {r.xlen( stream_key )}")
    print( f"after 10 sec block, got {l} new messages on the stream \n")

    return l



def writeStream2(stream2_key, ack):
    
    print( f"stream length before write: {r.xlen( stream2_key )}")
    print("-- writing on stream2")
    r.xadd(stream2_key, ack)

    print( f"stream length after write: {r.xlen( stream2_key )} \n")

'''
METHODS FOR COMMUNICATING DB-API-SIDE
'''

async def insertSelling(listtemp):
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        # es. i= {'nomeOgg': 'mioOgg1', 'prezzo': '208', 'quantità': '331', 'posizione': 'Oman'}
            # r1 = await client.schema("api").from_("ogginvendita").select("*").execute()
            # print("r.data \n", r1.data)
        for i in listtemp:
        #    for j in r.data: 
        #         if i["nomeOgg"]==j["nomeOgg"] and i["prezzo"]==j["prezzo"]:
        #             r = await client.schema("api").from_("ogginvendita").update({"quantità": str(int(j["quantità"])+int(i["quantità"])) }).execute()
        #         else:
            print("inserting item:", i)
            r2 = await client.schema("api").from_("ogginvendita").insert(i).execute()
            i["quantità"]=0
            # print("r2.data \n", r2.data)
            # print(r2.data[0]["id"])
            i["id"]=str(int(r2.data[0]["id"]))
            i["destinazione"] = ""
            r3 = await client.schema("api").from_("oggdaconsegn").insert(i).execute()
            i["tInvio"] = ""
            r4 = await client.schema("api").from_("oggconsegnati").insert(i).execute()
            
        return r   

'''
BEGIN OF MAIN
'''

# connect to redis
r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# del all ids entries from the stream
print("deleting \n")
for key in r.scan_iter():
    print(key)
    # delete the key
    r.delete(key)

# setup di hashMapServerLastID (vuota)
print("setup dell'hashmap serverLastIDTable\n")

# levare sotto?
r.hmset("hashMapServerLastID", {"Test":0})

print("Serverfornitore starting!\n")

while True:

    # itero su tutte le chiavi
    # print("Prossima iterazione\n")

    for key in r.scan_iter("*IN"):
        # print(key)
        
        # check se skeySIN è in hashmap, se non c'è salvo coppia (skeySIN:0)
        if key not in r.hgetall("hashMapServerLastID"):
            r.hset("hashMapServerLastID", key, 0)

            # debugg
            print(r.hget("hashMapServerLastID", key))

        messageDiz={}
        ll = readStreamOneMess(key)
        
        if (ll): # id l not empty

            # get data
            messageDiz=getEntryData2(ll)
            ack={"idRefToOrig": messageDiz.get("id"), "error": "False"}
            print(messageDiz, "\n")

            print("checking eventType\n")

            if messageDiz["eventType"]=="selling":
                print("eventType is selling\n")

                # aspetta che tutti gli altri messaggi (itemlist) vengano scritti su streamOUT
                time.sleep(2) # POTENZIALE VULNERABILITA (dipende da quanto ci mette il server a scrivere tutto itemlist)

                # leggi lista oggetti comprati da skeySIN
                zz = readStream(key)

                listtemp=getEntryData3(zz)
                print(listtemp)

                # richiedi db di aggiungi ogg in tabella diversa e aggiusta quantità

                temp = asyncio.run(insertSelling(listtemp))

                # ottieni skeySOUT
                print("ottieni skeySOUT")
                out=messageDiz["skeySOUT"]

                print("scrivo ack su stream2")
                finalAck={"ack": "SellingPlaced"}
                writeStream2(out, finalAck)
                # ack "error" = True se ci sono errori
                # manda ack a fornitore

    




