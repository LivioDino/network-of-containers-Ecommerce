#!/usr/bin/env python3
import matplotlib.pyplot as plt
import redis
import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import config

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

# errReq1=0
# errReq2=0
# errReq3=0

MAX_SEC_WAIT=10
MAX_OGG_DIVERSI= 5

# Requisiti funzionali che il monitor deve controllare:
# 1   messaggi su redis tra Cliente/serverCliente vengono effettuati in ordine cronologico (vedi schema)
# 2   il cliente aspetta max X secondi dall'invio della richesta al ricevimento (10s)
# 3   cliente compra massimo X articoli diversi, ovvero X entry diverse (5s)

# Requisiti non  funzionali che il monitor deve controllare:

# 4   rapporto clienti/quantità oggetti, oppure rapporto clienti/venditori/trasportatori è intorno a 40%/40%/20%
# 5   (opt) il cliente aspetta circa X secondi dall'invio della richesta al ricevimento (3s)
 
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
                if "OUT" in command["command"] and "id" in command["command"]:

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("OUT", "IN")

                    for line in loglist:
                        # print(line)

                        # check se Cliente ha mandato richiesta itemlist
                        if skkey not in line["command"]:
                            config.errReq1=1
                            print("error in 1.1")
                            break
                        else:
                            # se true, check se Cliente ha mandato richiesta itemlist prima di serverCliente manda itemlist
                            if line["time"] >= command["time"]:
                                config.errReq1=1
                                print("time error in 1.1")
                                break

                            # req 2.1 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= MAX_SEC_WAIT:
                                config.errReq2=1
                                print("time error in 2.1")
                                break

                            

                # req 1.2 (se Cliente manda purchase allora...)
                if "eventType purchase" in command["command"]:

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("IN", "OUT")

                    for line in loglist:
                        # print(line)

                        # check se serverCli ha mandato itemlist (almeno 1 ogg)
                        if skkey not in line["command"]:
                            config.errReq1=1
                            print("error in 1.2")
                            break
                        else:
                            # se true, check se serverCli ha mandato itemlist prima di "request purchase"
                            if line["time"] >= command["time"]:
                                config.errReq1=1
                                print("time error in 1.2")
                                break

                # req 1.3 (se serverCliente manda ack allora...)
                if "ack" in command["command"]:

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("OUT", "IN")

                    for line in loglist:
                        # print(line)

                        # check se Cliente ha mandato richiesta purchase
                        if skkey not in line["command"] or "id" not in line["command"]:
                            config.errReq1=1
                            print("error in 1.3")
                            break
                        else:
                            # se true, check se Cliente ha mandato richiesta purchase prima di serverCliente manda itemlist
                            if line["time"] >= command["time"]:
                                config.errReq1=1
                                print("time error in 1.3")
                                break

                            # req 2.2 (se Cliente aspetta più di x secondi allora ...)
                            if command["time"] - line["time"] >= MAX_SEC_WAIT:
                                config.errReq2=1
                                print("time error in 2.2")
                                break
                            

                

                # req 3
                if "ack" in command["command"]:

                    count=0

                    # prendo la chiave
                    t= command["command"].split(" ")
                    skkey=t[1].replace("OUT", "IN")

                    for line in loglist:
                        # print(line)

                        if skkey in line["command"] and "id" in line["command"]:
                            count+=1
                    
                    if count > MAX_OGG_DIVERSI:
                        config.errReq3=1

if __name__ == "__main__":
    main()