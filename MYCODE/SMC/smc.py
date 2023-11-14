#!/usr/bin/env python3


"""
BRAINSTORMING

cosa deve fare Statistical model checking? effettua multiple run:
occorre salvare i valori di Err generati dal monitor in una tabella specifica sul db.
All'inizio di una run creo un ennupla nel db con una chiave id serial, salvare il seed della run
    per seed della run conviene generalo in smc.py, poi mandarlo tra i generatori
Durante la run se il monitor modifica Err, porto le modifiche sul db
Al termine della singola run (di durata X costante per tutte le run), prendo valori Err dal db e li passo a SMC
SMC controlla tramite formula il rapporto

- Come si relazionano i req 6 e 7 in monitor con SMC? in ogni run bisogna "creare i scenari in cui clienti/venditori/trasportatori sono 0/pochi/molti" ?
- sotto che forma rmi conviene riportare il controesempio? instantanea del log del monitor + eventuale situazione del plotting?
- capire come utilizzare la formula finale
"""

import random
from postgrest import AsyncPostgrestClient
import asyncio
import time
from timeit import default_timer as timer
import math
import datetime
import subprocess
from smcTEST import *

# SPOSTARE SU MONITOR?
# for taking errAllReq.value from monitor at runtime (problem with docker?)
# import MYCODE.Monitor.monitor as monitor
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import varConfig as vcfg

DELTA= 0.001 
EPSILON= 0.001
TOTAL_RUNS=int(math.log(DELTA)/ math.log(1 - EPSILON))   # exstablish number of runs
TIME_HORIZON_SECONDS= 1000

def DockerTurnOn():
        
        print("launching docker-compose up")
        # DockerProc = subprocess.run(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE/MYCODE; echo 0000 | sudo -S docker-compose up -e VARGENCLI=myseed my_service"],  shell=True)
        DockerProc = subprocess.run(["docker-compose up"],  shell=True)

        print(DockerProc)

def DockerTurnOff():
        
        print("launching docker-compose down")
        # DockerProc = subprocess.run(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE/MYCODE; echo 0000 | sudo -S docker-compose up -e VARGENCLI=myseed my_service"],  shell=True)
        DockerProc = subprocess.run(["docker-compose down"],  shell=True)

        print(DockerProc)

# async def selectErrors(myseed):
#     async with AsyncPostgrestClient("http://localhost:3000") as client:
#         r = await client.schema("api").from_("monitorerrors").select("*").eq("seed", myseed).execute()
#         return r   
    
async def insertSeedRun(myseed):
    diz={"seed": str(myseed), "errallreq":0, "errtime":""}
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        r = await client.schema("api").from_("monitorerrors").insert(diz).execute()
        return r  
    
async def updateErrorRun(myseed, errtime):
    async with AsyncPostgrestClient("http://localhost:3000") as client:    
        r = await client.schema("api").from_("monitorerrors").update({"errallreq": 1, "errtime": errtime}).eq("seed", myseed).execute()
        return r 

"""
MAIN
"""

for run in range(0, TOTAL_RUNS):

    # generate a different seed each run and send to generators 
    myseed = datetime.datetime.now().timestamp()
    vcfg.myseedVcfg = myseed
    # write entry on db with initial error values to 0
    
    temp=asyncio.run(insertSeedRun(myseed))

    # launch every container from scratch (docker-compose), pass seed to generators

    # PER LANCIARE CON ARGOMENTI
    # docker-compose run -e VARGENCLI=actual_value my_service

    DockerTurnOn()
    # # using smcTEST
    # proc = turnOn()
    # print(proc)

    #launches start time
    timeEnd = 0
    timeStart = timer()
    
    # check if it should stop
    while(True):

        # terminate network of container after TIME_HORIZON_SECONDS (docker stop)
        if (timeEnd - timeStart) > TIME_HORIZON_SECONDS:
            print("time elapsed > TIME_HORIZON_SECONDS")
            break

        # or check moniotr for error values
        elif vcfg.errAllReqVcfg.value==1:
            print("monitor errAllReq.value==1, updating db table monitorerrors")
            errtime = datetime.datetime.now()

            temp2=asyncio.run(updateErrorRun(myseed, errtime))
            print(temp2.data)
            break
        
        timeEnd = timer()

    DockerTurnOff()

    # # using smcTEST
    # proc = turnOff()
    # print(proc)