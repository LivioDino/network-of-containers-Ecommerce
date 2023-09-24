#!/usr/bin/env python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import redis
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import numpy as np

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

def myplot(errReq1, errReq2, errReq3, commandTimeReq2, lineTimeReq2):

    # connect to redis
    r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

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

        for key in r.scan_iter("*IN"):
            f1 += 1

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

def myPlotReq_1_2(errReq1, commandTimeReq2, lineTimeReq2):

    # connect to redis
    r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim([0.0, 100.0])
    xs = []
    ys = []
    xs2 = []
    ys2 = []
    
    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys, xs2, ys2):

        if i%2==0:
            t1=str(commandTimeReq2.value)
            f1= float(t1[-8:])
        else:
            t1=str(lineTimeReq2.value)
            f1= float(t1[-8:])

        # example 1694873473.913011

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
        plt.title('myPlotReq_1_2')
        plt.ylabel('tempo arrivo messaggi')
        plt.xlabel("intervallo aggiornamento plot")

    # Set up plot to call animate() function periodically    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2), interval=1000)
    plt.show()

    #    # close figure
    # plt.close(fig)

def myPlotReq_3(errReq3, OggDiversiCountReq3):

    # connect to redis
    r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

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
        f3=0
        for key in r.scan_iter("*IN"): # count number of current Cliente
            f3 += 1
        
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
