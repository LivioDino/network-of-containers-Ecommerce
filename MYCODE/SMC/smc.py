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
import math


DELTA= 0.001 
EPSILON= 0.001
TOTAL_RUNS=math.log(DELTA)/ math.log(1 - EPSILON)   # exstablish number of runs
TIME_HORIZON_SECONDS= 1000


async def selectErrors(myseed):
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        r = await client.schema("api").from_("monitorerrors").select("*").eq("seed", myseed).execute()
        return r   
    
async def insertSeedRun(diz):
    async with AsyncPostgrestClient("http://localhost:3000") as client:
        r = await client.schema("api").from_("monitorerrors").insert(diz).execute()
        return r  

"""
MAIN
"""

for run in range(0,TOTAL_RUNS):
    totalErrors=[]

    # generate a different seed each run and send to generators 
    myseed = random.randint(1, 100000)

    # write entry on db with initial error values to 0
    diz={"seed": str(myseed), "error":"0"}
    temp=asyncio.run(insertSeedRun(diz))

    # launch every container from scratch (docker start)
        # terminate prematurely if monitor gives error

    # terminate network of container after TIME_HORIZON_SECONDS (docker stop)
    time.sleep(TIME_HORIZON_SECONDS)

    # check db for moniotr error values
    temp = asyncio.run(selectErrors(myseed))
    errors=temp.data
    print("errors:\n", errors)

    # add errors to totalErrors
    totalErrors.append(errors)