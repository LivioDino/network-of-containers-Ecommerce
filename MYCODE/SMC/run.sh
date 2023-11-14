#!/bin/bash
cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/DB

# to start db
sudo docker start tutorial

# to start the 3 redis instances

sudo systemctl start redis-server.service
sudo systemctl start redis-server2.service
sudo systemctl start redis-server3.service

# to start postgrest API (in directory MYCODE/DB)

./postgrest tutorial.conf

# to start different python 

python3 /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/Monitor/monitor.py