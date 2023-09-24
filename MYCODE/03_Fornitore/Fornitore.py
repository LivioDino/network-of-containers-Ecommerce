#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import MYREDISconfig as cfg

REDIS_HOSTNAME=cfg.REDIS_HOSTNAME_S3
REDIS_PORT=cfg.REDIS_PORT_S3
REDIS_PASSWORD=cfg.REDIS_PASSWORD_S3

sleeptime = 4
last_id_returned=0

import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import uuid

def connectToRedis():
    rr = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    return rr

def readACKStreamOld(stream2_key):
     
    print( f"stream length: {r.xlen( stream2_key )}")
    print("- waiting 10 sec for new messages on stream2")

    # wait for 10s for new message
    ll = r.xread( count=5, block=10000, streams={stream2_key: '$'} )
    print( f"stream length: {r.xlen( stream2_key )}")
    print( f"after 10 sec block, got {ll} new messages on the stream2 \n")
    return ll

def readStream2(stream2_key):
 
    print( f"stream length: {r.xlen( stream2_key )}")
    print("- reading from stream2")
    #(vede il primo messaggio in streamOUT, non li analizzo, bloccante)
    r.xread( count=1, block=10000, streams={stream2_key: '$'} )

    # aspetta che tutti gli altri messaggi (itemlist) vengano scritti su streamOUT
    time.sleep(2) # POTENZIALE VULNERABILITA (dipende da quanto ci mette il server a scrivere tutto itemlist)

    global last_id_returned
    print("last_id_returned", last_id_returned)
    print( f"stream length: {r.xlen( stream2_key )}")
    l = r.xread( count=100000, streams={stream2_key: last_id_returned} )
    print(l)
    if (l): # il not empty
        # for id, value in l[0][1]:
        #     print( f"id: {id} value: {value[b'v']}")
        last_id_returned = l[0][1][-1][0]
        print( f"stream length: {r.xlen( stream2_key )}")
    
    return l

def getEntryData2(ll):
    print("- getting entry data")
    [[stream, [[id, values]]]] = ll
    diz=dict(values)
    diz["id"]=id
    return diz

def getEntryData3(l):
    print("- getting entry data")
    listdiz=[]
    for i in l[0][1]:
        # print(i)
        # print(i[1])
        listdiz.append(i[1])

    return listdiz

def writeStream(stream_key, event):
    
    print( f"stream length before write: {r.xlen( stream_key )}")
    print("- writing on stream")
    r.xadd(stream_key, event)
    print( f"stream length after write: {r.xlen( stream_key )} \n")

def delMessages(stream_key): # non usato
    print("- deleting all ids entries from the stream \n")

    s1 = r.xread( streams={stream_key:0} )
    for streams in s1:
        stream_name, messages = streams

    [ r.xdel( stream_name, i[0] ) for i in messages ]


def requestItemList(stream_key, stream2_key):
    # genra evento Itemlist e manda su stream
    print("- requesting fornitore item list")
    event = {"eventType": "itemlist", "condition":"", "skeySOUT":stream2_key}
    writeStream(stream_key, event)

    # aspetta ack su stream 2
    l = readStream2(stream2_key)

    listdiz=getEntryData3(l)
    print(listdiz)

    return listdiz
    

def requestPurchase(itemListNEW, stream_key, stream2_key):
    # evento da definire dopo aver ricevito ItemList
    print("- requesting fornitore purchase")
    event = {"eventType": "purchase", "skeySOUT":stream2_key}

    writeStream(stream_key, event)
    for mess in itemListNEW:
        writeStream(stream_key, mess)
        
    # aspetta ack su stream 2
    l = readStream2(stream2_key)

def createStreams():
    # genero id unico (usa indirizzo mac + timestamp)
    uniqueid = str(uuid.uuid1())
    print ("The random id using uuid1() is :", uniqueid)

    # crea nuova stream di output (skey) e input (skey2)
    
    skeySIN = uniqueid + "_SIN"
    skeySOUT = uniqueid + "_SOUT"
    print ("creo 2 nuove streams vuote con key:\n")
    print (skeySIN)
    print (skeySOUT, "\n")

    entryTest= {"test":0}
    writeStream(skeySIN, entryTest)
    writeStream(skeySOUT, entryTest)

    delMessages(skeySIN)
    delMessages(skeySOUT)

    print("CHECK: len delle stream(deve essere 00):", r.xlen(skeySIN), r.xlen(skeySOUT))

def createStreams_V2():
    # genero id unico (usa indirizzo mac + timestamp)
    uniqueid = str(uuid.uuid1())
    print ("The random id using uuid1() is :", uniqueid)

    # crea nuova stream di output (skey) e input (skey2)
    
    skeySIN = uniqueid + "_SIN"
    skeySOUT = uniqueid + "_SOUT"
    print ("creo 2 nuove streams vuote con keys:")
    print (skeySIN)
    print (skeySOUT, "\n")

    return(skeySIN, skeySOUT)

if __name__ == '__main__':
    '''
    BEGIN OF MAIN
    '''

# apre connessione "r" a redis
r = connectToRedis()

# definire 2 stream su redis (skeySIN e skeySOUT)
tuple=createStreams_V2()

# richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
itemList= requestItemList(tuple[0], tuple[1]) #(skeySIN e skeySOUT)

# TEST ONLY fornitore ordina meta della lista originale
half = len(itemList)//2
itemListNEW=[]
for i in itemList[:half]:
    i["quantità"]=5
    itemListNEW.append(i)

print(itemListNEW)

requestPurchase(itemListNEW, tuple[0], tuple[1])

# alla fine elimina le proprie stream

r.delete(tuple[0]) # skeySIN
r.delete(tuple[1]) # skeySOUT