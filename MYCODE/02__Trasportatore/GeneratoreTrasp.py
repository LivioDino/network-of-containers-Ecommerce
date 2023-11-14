#!/usr/bin/env python3
import time
import random
from multiprocessing import Process
from time import sleep
from Trasportatore import *
from importlib import reload
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import varConfig as vcfg

# generatore crea eventi random:
# "arrivo" trasportatore
# quantità ogg trasportati

CYCLE= [5.0, 10.0, 20.0] #INTERVALLO_MAX_CLIENTE_LOW_VOLUME=20.0    INTERVALLO_MAX_CLIENTE_MED_VOLUME=10.0  INTERVALLO_MAX_CLIENTE_HIGH_VOLUME=5.0
CYCLE_SWITCH_NUM=10
MAX_OGG_TRASPORTATI=5

def trasportFunction():

    # trasportatore si connette a redis
    r = connectToRedis()

    # definire 2 stream su redis (skeySIN e skeySOUT)
    tuple=createStreams_V2()

    caricoOgg = random.randint(1, MAX_OGG_TRASPORTATI)

    # richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
    itemList= requestTransport(caricoOgg, tuple[0], tuple[1], r) #(skeySIN e skeySOUT)

    # print(itemList)

    # alla fine elimina le proprie stream
    r.delete(tuple[0]) # skeySIN
    r.delete(tuple[1]) # skeySOUT

if __name__ == '__main__':

    '''
    BEGIN OF MAIN
    '''
    iterCount=0 
    cycleIter=0  
    IntervalloMax=0.0

    if len( sys.argv ) > 1:
        random.seed(sys.argv[1]) # set the seed for the run
        print("seed set:", sys.argv[1])

    if vcfg.myseedVcfg != 0:
        random.seed(vcfg.myseedVcfg) # set the seed for the run
        print("seed set myseedVcfg:", vcfg.myseedVcfg)

    while True:
        
        # ogni CYCLE_SWITCH_NUM clienti/fornitori/trasportatori cambia la frequenza di arrivo con intervallo max, cicla i valori in CYCLE
        if iterCount % CYCLE_SWITCH_NUM==0:
            IntervalloMax = CYCLE[cycleIter]
            cycleIter = (cycleIter+1) % len(CYCLE)
            print("IntervalloArrivo", IntervalloMax)

        iterCount+=1

        # generate when next trasportatore arrives
        tarrivo = random.uniform(1.0, IntervalloMax)
        print("- Main : waiting for new trasportatore")
        time.sleep(tarrivo)

        print("-- Main : arrivo nuovo trasportatore, dopo: ", tarrivo, "\n\n")

        # crea enevtualmente nuovo processo per gestire operazioni trasportatore
        print("- launching trasportFunction in new child process")
        process = Process(target=trasportFunction, daemon=True) # deamon=True per terminare i figli in caso il processo main termina in modo anomalo
        process.start()
        
    print("join process")
    process.join()



