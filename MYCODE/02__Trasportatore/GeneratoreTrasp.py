#!/usr/bin/env python3
import time
import random
from multiprocessing import Process
from time import sleep
from Trasportatore import *
from importlib import reload

# generatore crea eventi random:
# "arrivo" trasportatore

INTERVALLO_MAX_TRASPORTATORE=10.0

def trasportFunction():

    # trasportatore si connette a redis
    r = connectToRedis()

    # definire 2 stream su redis (skeySIN e skeySOUT)
    tuple=createStreams_V2()

    # richiede a server lista oggetti (manada a server richiesta su skeySIN, riceve lista di diz su skeySOUT)
    itemList= requestTransport(tuple[0], tuple[1]) #(skeySIN e skeySOUT)

    print(itemList)

    # alla fine elimina le proprie stream
    r.delete(tuple[0]) # skeySIN
    r.delete(tuple[1]) # skeySOUT

if __name__ == '__main__':

    '''
    BEGIN OF MAIN
    '''
        
    while True:
        
        # generate when next trasportatore arrives
        tarrivo = random.uniform(0.0, INTERVALLO_MAX_TRASPORTATORE)
        print("- Main : waiting for new trasportatore")
        time.sleep(tarrivo)

        print("-- Main : arrivo nuovo trasportatore, dopo: ", tarrivo, "\n\n")

        # crea enevtualmente nuovo processo per gestire operazioni trasportatore
        print("- launching trasportFunction in new child process")
        process = Process(target=trasportFunction, daemon=True) # deamon=True per terminare i figli in caso il processo main termina in modo anomalo
        process.start()
        
    print("join process")
    process.join()



