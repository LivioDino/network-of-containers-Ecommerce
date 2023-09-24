#!/usr/bin/env python3
import matplotlib.pyplot as plt
import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
from multiprocessing import Process, Value
from liveplotNEW import *

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

errReq1=Value('i', 0) # error flag for req1
errReq2=Value('i', 0) # error flag for req2
errReq3=Value('i', 0) # error flag for req3
errReq4=Value('i', 0) # error flag for req4
errReq5=Value('i', 0) # error flag for req5
errReq6=Value('i', 0) # error flag for req6

commandTimeReq2=Value('d', 0.0)
lineTimeReq2=Value('d', 0.0)
OggDiversiCountReq3=Value('i', 0)
tempErr=Value('i', 0)


MAX_SEC_WAIT=10 # for req2
IDEAL_SEC_WAIT=3 # for req5
MAX_OGG_DIVERSI= 5 # for req3

# Requisiti funzionali che il monitor deve controllare: (CONTROLALRE TERMINOLGIA)
# 1   I messaggi tra Cliente e serverCliente vengono inviato attraverso redis in ordine cronologico corretto, ovvero ogni messaggio deve essere inviato solo dopo la precedente richiesta corrispondente (vedi schema)
# 2   Dall'invio di una richiesta del Cliente alla recezione della corretta risposta, inviata da ServerCliente, devono passare massimo X secondi (10s) (caso 1,2 e 3,4 schema)
# 3   Ogni Cliente puoò comprare massimo X articoli diversi per ogni ordine (5)

# Requisiti non funzionali che il monitor deve controllare:

# 4   Il rapporto clienti/quantità oggetti nel db, oppure rapporto clienti/venditori/trasportatori è intorno a 40%/40%/20%
# 5   Dall'invio di una richiesta del Cliente alla recezione della corretta risposta, inviata da ServerCliente, devono passare massimo X secondi (3s) (caso 1,2 e 3,4 schema)
# 6   il sistema deve funzionare con scenari in cui clienti/venditori/trasportatori sono 0/pochi/molti 
 
def main():
        
    r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    # inizio monitor
    print("starting monitor!")

    # inizio checking requirements conditions
    print("checking requirements conditions")

    loglist=[]
    with r.monitor() as m:

        for command in m.listen():
        # scan for every command sent to redis

            # aggiungo al log
            if "XADD " in command["command"]:
                print(command)
                loglist.append(command)

                # req 1.1 (se serverCliente manda itemlist allora...)
                if "OUT " in command["command"] and "id " in command["command"]:

                    OggDiversiCountReq3.value=0 # solo a scopo grafico, resetta count ogg 

                    # prendo la chiave
                    t= command["command"].split(" ")
                    # print("t:", t)
                    skkey=t[1].replace("OUT", "IN")
                    # print("skkey:", skkey)

                    tempErr.value=1 # setto tempErr a true finche non trovo la linea nel log che cerco
                    for line in loglist:
                        # print(line)

                        # check se Cliente ha mandato richiesta itemlist
                        if skkey in line["command"] and "eventType itemlist" in line["command"]:
                            tempErr.value=0

                            # valori da mandare a live plot per plotting

                            # print("commandTimeReq2.value:", commandTimeReq2.value)
                            # print("lineTimeReq2.value;", lineTimeReq2.value)

                            commandTimeReq2.value=command["time"]
                            lineTimeReq2.value=line["time"]

                            # commandTimeReq2.value+=1
                            # lineTimeReq2.value+=1

                            # se true, check se Cliente ha mandato richiesta itemlist prima di serverCliente manda itemlist
                            if line["time"] >= command["time"]:
                                errReq1.value=1
                                print("time error in 1.1")
                                break

                            # req 2.1 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= MAX_SEC_WAIT:
                                errReq2.value=1
                                print("time error in 2.1")
                                break

                            # req 5.1 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= IDEAL_SEC_WAIT:
                                errReq5.value=1
                                print("time error in 5.1")
                                break

                    # finita iterazione su log, se non trova nel log request itemlist da parte di Cliente...
                    if tempErr.value==1:
                        errReq1.value=1
                        print("error in 1.1")

                            

                # req 1.2 (se Cliente manda purchase allora...)
                if "eventType purchase" in command["command"]:

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("IN", "OUT")

                    tempErr.value=1 # setto tempErr a true finche non trovo la linea nel log che cerco
                    for line in loglist:
                        # print(line)

                        # check se serverCli ha mandato itemlist (almeno 1 ogg)
                        if skkey in line["command"] and "id " in line["command"]:
                            tempErr.value=0

                            # se true, check se serverCli ha mandato itemlist prima di "request purchase"
                            if line["time"] >= command["time"]:
                                errReq1.value=1
                                print("time error in 1.2")
                                break

                    # finita iterazione su log, se non trova nel log request itemlist da parte di Cliente...
                    if tempErr.value==1:
                        errReq1.value=1
                        print("error in 1.2")


                # req 1.3 (se serverCliente manda ack allora...)
                if "ack" in command["command"]:

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("OUT", "IN")

                    tempErr.value=1 # setto tempErr a true finche non trovo la linea nel log che cerco
                    for line in loglist:
                        # print(line)

                        # check se Cliente ha mandato richiesta purchase
                        if skkey in line["command"] and "eventType itemlist" in line["command"]:
                            tempErr.value=0

                            # valori da mandare a live plot per plotting

                            # print("commandTimeReq2.value:", commandTimeReq2.value)
                            # print("lineTimeReq2.value;", lineTimeReq2.value)

                            commandTimeReq2.value=command["time"]
                            lineTimeReq2.value=line["time"]

                            # commandTimeReq2.value+=1
                            # lineTimeReq2.value+=1

                            # se true, check se Cliente ha mandato richiesta purchase prima di serverCliente manda itemlist
                            if line["time"] >= command["time"]:
                                errReq1.value=1
                                print("time error in 1.1")
                                break

                            # req 2.2 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= MAX_SEC_WAIT:
                                errReq2.value=1
                                print("time error in 2.2")
                                break

                            # req 5.2 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= IDEAL_SEC_WAIT:
                                errReq5.value=1
                                print("time error in 5.2")
                                break

                    # finita iterazione su log, se non trova nel log request itemlist da parte di Cliente...
                    if tempErr.value==1:
                        errReq1.value=1
                        print("error in 1.3")

                # req 3
                if "ack" in command["command"]:

                    OggDiversiCountReq3.value=0

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("OUT", "IN")

                    for line in loglist:
                        # print(line)

                        if skkey in line["command"] and "id" in line["command"]:
                            OggDiversiCountReq3.value+=1
                    
                    if OggDiversiCountReq3.value > MAX_OGG_DIVERSI:
                        errReq3.value=1
                        print("error in 3")

if __name__ == "__main__":
    # creo processi per il live plotting

    # testp = Process(target=myplot, args=(errReq1, errReq2, errReq3, commandTimeReq2, lineTimeReq2), daemon=True)
    pReq_1_2 = Process(target=myPlotReq_1_2, args=(errReq1, commandTimeReq2, lineTimeReq2), daemon=True)
    pReq_3 = Process(target=myPlotReq_3, args=(errReq3, OggDiversiCountReq3), daemon=True)

    # lancio un nuovo processo per ogni liveplot
    pReq_1_2.start()
    time.sleep(1)
    pReq_3.start()

    # lancio main per controllare i requisti
    main()

    # joino processi (con daemon=True in pReq_1_2, vengono terminati i child al termine del padre)
    pReq_1_2.join()
    pReq_3.join()
    