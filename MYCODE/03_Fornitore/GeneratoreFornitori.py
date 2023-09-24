#!/usr/bin/env python3
import time
import random
from multiprocessing import Process
from time import sleep
from Fornitore import *
from importlib import reload

# generatore crea eventi random:
# "arrivo" fornitore, 
# se aquistare oggetti (dopo snapshot del db),
# scelta oggetti stessi

INTERVALLO_MAX_FORNITORE=10.0
PERC_CLIENTI_ACQUISTANTI=0.5
PERC_OGGETTI_DA_COMPRARE=0.2
MAX_QUANTITÀ_PER_OGGETTO=10
MAX_QUANTITÀ_OGGETTI_DIVERSI=5

def generaOggetti():
    # oggetti generati devono essere scelti dalla lista ritornata dal db (oovero post richiesta snapshot db)
    l=[]


def fornitFunction():

    # fornitore si connette a redis
    r = connectToRedis()

    # definire 2 stream su redis (skeySIN e skeySOUT)
    tuple=createStreams_V2()

    # richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
    itemList= requestItemList(tuple[0], tuple[1]) #(skeySIN e skeySOUT)

    # generate if fornitore buys items (aka if checks only items)
    compraBool = random.random() > PERC_CLIENTI_ACQUISTANTI
    print("fornitore compra ogg:", compraBool)

    if compraBool:
        # genera lista oggetti da snapsot db
        itemListNEW=[]
        for i in itemList:
            if random.random() > PERC_OGGETTI_DA_COMPRARE:
                i["quantità"]= random.randint(1, MAX_QUANTITÀ_PER_OGGETTO)
                itemListNEW.append(i)
                # se il fornitore sta comprando 5 oggetti diversi
                if len(itemListNEW) == MAX_QUANTITÀ_OGGETTI_DIVERSI:
                    break

        print(itemListNEW)

        # invia richiesta acquisto con lista ogg
        requestPurchase(itemListNEW, tuple[0], tuple[1])

    # alla fine elimina le proprie stream
    r.delete(tuple[0]) # skeySIN
    r.delete(tuple[1]) # skeySOUT

if __name__ == '__main__':

    '''
    BEGIN OF MAIN
    '''

    while True:
        
        # generate when next fornitore arrives
        tarrivo = random.uniform(0.0, INTERVALLO_MAX_FORNITORE)
        print("- Main : waiting for new fornitore")
        time.sleep(tarrivo)

        print("-- Main : arrivo nuovo fornitore, dopo: ", tarrivo, "\n\n")

        # crea enevtualmente nuovo processo per gestire operazioni fornitore
        print("- launching fornitFunction in new child process")
        process = Process(target=fornitFunction, daemon=True) # deamon=True per terminare i figli in caso il processo main termina in modo anomalo
        process.start()
        
    print("join process")
    process.join()



