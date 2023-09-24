#!/usr/bin/env python3
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import redis
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import numpy as np
from datetime import datetime

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


def myplot(errReq1, errReq2, errReq3, commandTimeReq2, lineTimeReq2): # non utilizzato (old)

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    xs2 = []
    ys2 = []

    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys, xs2, ys2):
        
        # count number of current cliente
        f1=0

        # for key in r.scan_iter("*IN"):
        #     f1 += 1

        # get error flag from monitor
        f2=errReq1.value

        # f1=lineTimeReq2.value
        # f2=errReq2.values

        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys.append(f1)
        xs2.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys2.append(f2)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        xs2 = xs2[-20:]
        ys2 = ys2[-20:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.plot(xs2, ys2)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Numero Clienti over Time')
        plt.ylabel('Clienti')

    # Set up plot to call animate() function periodically    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2), interval=500)
    plt.show()

def myPlotReq_1_2_5(errReq1, commandTimeReq2, lineTimeReq2):

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim([0.0, 10000000000.0])
    xs = []
    ys = []
    xs2 = []
    ys2 = []
    t=0.0
    
    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys, xs2, ys2, t):

        """
        # SOLUZIONE
                f2=errReq1.value + valore iniziale di time del messaggio (commandTimeReq2.value),
                cosi tutto il grafico si shifta su iniziale di commandTimeReq2.value invece che 0
                in teoria i valori reali di time # example 1694873473.913011 li fa vedere a "scaletta"

        """

        if i%2==0:
            timestamp = lineTimeReq2.value
        else:
            timestamp = commandTimeReq2.value

        # timestamp = commandTimeReq2.value
        date_time = datetime.fromtimestamp(timestamp)
        f1 = date_time.strftime("%M:%S:%f")

        # get error flag from monitor
        f2=errReq1.value

        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys.append(f1)
        xs2.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys2.append(f2)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        xs2 = xs2[-20:]
        ys2 = ys2[-20:]


        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.plot(xs2, ys2)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('myPlotReq_1_2_5')
        plt.ylabel('tempo arrivo messaggi')
        plt.xlabel("intervallo aggiornamento plot")

    # Set up plot to call animate() function periodically    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2, t), interval=1000)
    plt.show()

    #    # close figure
    # plt.close(fig)

def myPlotReq_3(errReq3, OggDiversiCountReq3, countClienti):

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim([0.0, 100.0])
    xs = []
    ys = []
    xs2 = []
    ys2 = []
    xs3 = []
    ys3 = []
    
    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys, xs2, ys2, xs3, ys3):

        # establishing factor values

        f1 = OggDiversiCountReq3.value #count diffrent objects from Cliente
        f2=errReq3.value # get error flag from monitor        
        f3=countClienti.value
        
        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys.append(f1)
        xs2.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys2.append(f2)
        xs3.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys3.append(f3)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        xs2 = xs2[-20:]
        ys2 = ys2[-20:]
        xs3 = xs3[-20:]
        ys3 = ys3[-20:]


        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.plot(xs2, ys2)
        ax.plot(xs3, ys3)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('myPlotReq_3')
        plt.ylabel('count oggetti div. per Cliente')
        plt.xlabel("intervallo aggiornamento plot")

    # Set up plot to call animate() function periodically    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2, xs3, ys3), interval=1000)
    plt.show()

    #    # close figure
    # plt.close(fig)

def myplotReq_6_7(errAllReq, countClienti, countTrasportatori, countFornitori):

    r = redis.Redis(host=REDIS_HOSTNAME_S1, port=REDIS_PORT_S1, password=REDIS_PASSWORD_S1, decode_responses=True)
    r2 = redis.Redis(host=REDIS_HOSTNAME_S2, port=REDIS_PORT_S2, password=REDIS_PASSWORD_S2, decode_responses=True)
    r3 = redis.Redis(host=REDIS_HOSTNAME_S3, port=REDIS_PORT_S3, password=REDIS_PASSWORD_S3, decode_responses=True)

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    xs2 = []
    ys2 = []
    xs3 = []
    ys3 = []
    xs4 = []
    ys4 = []

    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys, xs2, ys2, xs3, ys3, xs4, ys4):
        
        # count number of current clienti
        countClienti.value = 0
        for key in r.scan_iter("*IN"):
            countClienti.value += 1

        # count number of current transportatori
        countTrasportatori.value=0
        for key in r2.scan_iter("*IN"):
            countTrasportatori.value += 1

        # count number of current fornitori
        countFornitori.value=0
        for key in r3.scan_iter("*IN"):
            countFornitori.value += 1

        f1=countClienti.value 
        f2=errAllReq.value
        f3=countTrasportatori.value
        f4=countFornitori.value

        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys.append(f1)
        xs2.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys2.append(f2)
        xs3.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys3.append(f3)
        xs4.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys4.append(f4)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        xs2 = xs2[-20:]
        ys2 = ys2[-20:]
        xs3 = xs3[-20:]
        ys3 = ys3[-20:]
        xs4 = xs4[-20:]
        ys4 = ys4[-20:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.plot(xs2, ys2)
        ax.plot(xs3, ys3)
        ax.plot(xs4, ys4)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('myplotReq_6_7')
        plt.ylabel('Clienti')

    # Set up plot to call animate() function periodically    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2, xs3, ys3, xs4, ys4), interval=500)
    plt.show()