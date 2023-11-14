#!/usr/bin/env python3
import matplotlib.pyplot as plt
import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
from multiprocessing import Process, Value
from liveplot import *

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import MYREDISconfig as cfg

# redis-server (lato cliente)
REDIS_HOSTNAME_S1=cfg.REDIS_HOSTNAME_S1
REDIS_PORT_S1=cfg.REDIS_PORT_S1
REDIS_PASSWORD_S1=cfg.REDIS_PASSWORD_S1

# redis-server2 (lato trasportatore)
REDIS_HOSTNAME_S2=cfg.REDIS_HOSTNAME_S2
REDIS_PORT_S2=cfg.REDIS_PORT_S2
REDIS_PASSWORD_S2=cfg.REDIS_PASSWORD_S2

# redis-server3 (lato fornitore)
REDIS_HOSTNAME_S3=cfg.REDIS_HOSTNAME_S3
REDIS_PORT_S3=cfg.REDIS_PORT_S3
REDIS_PASSWORD_S3=cfg.REDIS_PASSWORD_S3

errReq1=Value('i', 0) # error flag for req1
errReq2=Value('i', 0) # error flag for req2
errReq3=Value('i', 0) # error flag for req3
# errReq4=Value('i', 0) # error flag for req4
errReq5=Value('i', 0) # error flag for req5
errReq6=Value('i', 0) # error flag for req6
errAllReq=Value('i', 0) # error flag for all requisites together 

commandTimeReq2=Value('d', 0.0)
lineTimeReq2=Value('d', 0.0)
OggDiversiCountReq3=Value('i', 0)
tempErr=Value('i', 0)

countClienti=Value('i', 0)
countTrasportatori=Value('i', 0)
countFornitori=Value('i', 0)

MAX_SEC_WAIT=10 # for req2
IDEAL_SEC_WAIT=3 # for req5
MAX_OGG_DIVERSI= 5 # for req3

# Requisiti funzionali che il monitor deve controllare: (CONTROLALRE TERMINOLGIA)
# 1   I messaggi tra Cliente e serverCliente vengono inviato attraverso redis in ordine cronologico corretto, ovvero ogni messaggio deve essere inviato solo dopo la precedente richiesta corrispondente (vedi schema)
# 2   Dall'invio di una richiesta del Cliente alla recezione della corretta risposta, inviata da ServerCliente, devono passare massimo X secondi (10s) (caso 1,2 e 3,4 schema)
# 3   Ogni Cliente può comprare massimo X articoli diversi per ogni richiesta (5)
# 4(opt)   Ogni Fornitore può vendere massimo X articoli diversi per ogni richiesta (5)

# Requisiti non funzionali che il monitor deve controllare:

# 5   Dall'invio di una richiesta del Cliente alla recezione della corretta risposta, inviata da ServerCliente, devono passare massimo X secondi (3s) (caso 1,2 e 3,4 schema)
# 6   il sistema deve funzionare in uno scenario in cui clienti/venditori/trasportatori sono in quantità equa generata casualmente
# 7   il sistema deve funzionare in scenari in cui clienti/venditori/trasportatori sono 0/pochi/molti 
 
def main():
     
        
    r = redis.Redis(host=REDIS_HOSTNAME_S1, port=REDIS_PORT_S1, password=REDIS_PASSWORD_S1, decode_responses=True)
    r2 = redis.Redis(host=REDIS_HOSTNAME_S2, port=REDIS_PORT_S2, password=REDIS_PASSWORD_S2, decode_responses=True)
    r3 = redis.Redis(host=REDIS_HOSTNAME_S3, port=REDIS_PORT_S3, password=REDIS_PASSWORD_S3, decode_responses=True)

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
                        if skkey in line["command"] and "eventType purchase" in line["command"]:
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
                    # commandTimeReq2.value=0.0
                    # lineTimeReq2.value=0.0
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



            # req 6 e 7

            # se almeno un errore di un requisito ha valore 1 (ovvero True)
            if not (errReq1.value==0 and errReq2.value==0 and errReq3.value==0):
                errAllReq.value==1

            # # count number of current clienti
            # countClienti.value = 0
            # for key in r.scan_iter("*IN"):
            #     countClienti.value += 1

            # # count number of current transportatori
            # countTrasportatori.value=0
            # for key in r2.scan_iter("*IN"):
            #     countTrasportatori.value += 1

            # # count number of current fornitori
            # countFornitori.value=0
            # for key in r3.scan_iter("*IN"):
            #     countFornitori.value += 1

if __name__ == "__main__":
    # creo processi per il live plotting

    # testp = Process(target=myplot, args=(errReq1, errReq2, errReq3, commandTimeReq2, lineTimeReq2), daemon=True)
    pReq_1_2_5 = Process(target=myPlotReq_1_2_5, args=(errReq1, commandTimeReq2, lineTimeReq2), daemon=True)
    pReq_3 = Process(target=myPlotReq_3, args=(errReq3, OggDiversiCountReq3, countClienti), daemon=True)
    pReq_6_7 = Process(target=myplotReq_6_7, args=(errAllReq, countClienti, countTrasportatori, countFornitori), daemon=True)

    # lancio un nuovo processo per ogni liveplot
    pReq_1_2_5.start()
    time.sleep(0.5)
    pReq_3.start()
    time.sleep(0.5)
    pReq_6_7.start()

    # lancio main per controllare i requisti
    main()

    # joino processi (con daemon=True in pReq_1_2_5, vengono terminati i child al termine del padre)
    pReq_1_2_5.join()
    pReq_3.join()
    pReq_6_7.join()
    