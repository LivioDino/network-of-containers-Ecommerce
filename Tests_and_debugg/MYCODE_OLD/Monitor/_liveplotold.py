#!/usr/bin/env python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import redis
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError

REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
REDIS_PORT="17843"
REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

# connect to redis
r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    
    temp_c=0
    
    for key in r.scan_iter("*IN"):
        temp_c += 1

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%M:%S')) # '%H:%M:%S.%f'
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Numero Clienti over Time')
    plt.ylabel('Clienti')

# Set up plot to call animate() function periodically
    
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=500)
plt.show()
