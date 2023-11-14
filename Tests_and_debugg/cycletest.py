
CYCLE= [5.0, 10.0, 20.0] #INTERVALLO_MAX_CLIENTE_LOW_VOLUME=20.0    INTERVALLO_MAX_CLIENTE_MED_VOLUME=10.0  INTERVALLO_MAX_CLIENTE_HIGH_VOLUME=5.0


iterCount=0 
cycleIter=0  
IntervalloMax=0.0

while True:

    if iterCount%10==0:
        IntervalloMax = CYCLE[cycleIter]
        cycleIter = (cycleIter+1) % len(CYCLE)
        print(IntervalloMax)

    iterCount+=1
    print("iterCount", iterCount)



