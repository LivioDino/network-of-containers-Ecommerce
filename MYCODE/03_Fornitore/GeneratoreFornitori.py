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
MAX_QUANTITÀ_PER_OGGETTO=1000
MAX_PREZZO_PER_OGGETTO=1000
MAX_OGGETTI_DIVERSI=5
LISTA_NOMI_TOT=["Wallet","Slipper","Washcloth","Door","House","Egg","Mp3 player","Shampoo","Plate","Rubber band","Crow","Bouquet of flowers"]
LISTA_POSIZIONI_TOT=["Braavlurgh","Slazloit","Ribrada","Akrucadena","Fleflance","Fokosa","Kavouis","Guecrando","Ruohock","Kroework","Izhuukrico","Oklekok"]

def generaOggetti():
    # oggetti generati devono essere scelti dalla lista ritornata dal db (oovero post richiesta snapshot db)
    l=[]


def fornitFunction():

    # fornitore si connette a redis
    r = connectToRedis()

    # definire 2 stream su redis (skeySIN e skeySOUT)
    tuple=createStreams_V2()

    # richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
    itemListNEW=[]

    for i in range(0,MAX_OGGETTI_DIVERSI):
        ogg={'nomeOgg': '', 'prezzo': '', 'quantità': '', 'posizione': ''}
        ogg["nomeOgg"]=random.choice(LISTA_NOMI_TOT)
        ogg["prezzo"]= random.randint(1, MAX_PREZZO_PER_OGGETTO)
        ogg["quantità"] = random.randint(1, MAX_QUANTITÀ_PER_OGGETTO)
        ogg["posizione"]=random.choice(LISTA_POSIZIONI_TOT)
        itemListNEW.append(ogg)
        
    # es. itemList=[{'nomeOgg': 'mioOgg1', 'prezzo': '208', 'quantità': '331', 'posizione': 'Oman'},
    #            {'nomeOgg': 'mioOgg2', 'prezzo': '372', 'quantità': '36', 'posizione': 'Berlino'},
    #            {'nomeOgg': 'mioOgg3', 'prezzo': '11', 'quantità': '539', 'posizione': 'Roma'}]

    print(itemListNEW)

    # invia richiesta acquisto con lista ogg
    requestSelling(itemListNEW, tuple[0], tuple[1])

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



