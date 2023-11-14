#!/usr/bin/env python3
import time
import random
from multiprocessing import Process
from time import sleep
from Cliente import *
from importlib import reload
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import varConfig as vcfg


# generatore crea eventi random:
# "arrivo" cliente, 
# se aquistare oggetti (dopo snapshot del db),
# scelta oggetti stessi

CYCLE= [5.0, 10.0, 20.0] #INTERVALLO_MAX_CLIENTE_LOW_VOLUME=20.0    INTERVALLO_MAX_CLIENTE_MED_VOLUME=10.0  INTERVALLO_MAX_CLIENTE_HIGH_VOLUME=5.0
CYCLE_SWITCH_NUM=10
PERC_CLIENTI_ACQUISTANTI=0.5
PERC_OGGETTI_DA_COMPRARE=0.2
MAX_QUANTITÀ_PER_OGGETTO=10
MAX_OGGETTI_DIVERSI=5
  
def generaOggetti():
    # oggetti generati devono essere scelti dalla lista ritornata dal db (oovero post richiesta snapshot db)
    l=[]


def clientFunction():

    # cliente si connette a redis
    r = connectToRedis()

    # definire 2 stream su redis (skeySIN e skeySOUT)
    tuple=createStreams_V2()

    # richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
    itemList= requestItemList(tuple[0], tuple[1], r) #(skeySIN e skeySOUT)

    # generate if cliente buys items (aka if checks only items)
    compraBool = random.random() > PERC_CLIENTI_ACQUISTANTI
    print("Cliente compra ogg:", compraBool)

    if compraBool:
        # genera lista oggetti da snapsot db
        itemListNEW=[]
        for i in itemList:
            if random.random() > PERC_OGGETTI_DA_COMPRARE:
                i["quantità"]= random.randint(1, MAX_QUANTITÀ_PER_OGGETTO)
                itemListNEW.append(i)
                # se il Cliente sta comprando 5 oggetti diversi
                if len(itemListNEW) == MAX_OGGETTI_DIVERSI:
                    break

        print(itemListNEW)

        # invia richiesta acquisto con lista ogg
        requestPurchase(itemListNEW, tuple[0], tuple[1], r)

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

        # generate when next cliente arrives
        tarrivo = random.uniform(1.0, IntervalloMax)
        print("- Main : waiting for new cliente")
        time.sleep(tarrivo)

        print("-- Main : arrivo nuovo cliente, dopo: ", tarrivo, "\n\n")

        # crea enevtualmente nuovo processo per gestire operazioni cliente
        print("- launching clientFunction in new child process")
        process = Process(target=clientFunction, daemon=True) # deamon=True per terminare i figli in caso il processo main termina in modo anomalo
        process.start()
        
    print("join process")
    process.join()



