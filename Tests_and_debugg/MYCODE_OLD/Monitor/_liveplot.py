#!/usr/bin/env python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import redis
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
import MYCODE.Monitor._monitor as _monitor

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

def myplot():

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
        # f2=config.errReq1


        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        ys.append(f1)

        xs2.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
        # ys2.append(f2)

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

if __name__ == "__main__": 
    myplot()