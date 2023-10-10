# to start db 

sudo docker start tutorial

# to start postgrest API (in directory MYCODE/DB)
./postgrest tutorial.conf

# to start the 3 redis instances

sudo systemctl start redis-server.service
sudo systemctl start redis-server2.service
sudo systemctl start redis-server3.service

# per pushare su github (in directory network-of-ECOMMERCE)
git push origin main

-------------------------------------------

# check redis active instances
ps aux |grep redis

sudo lsof -i -P -n | grep 5433  # List who's using the port
sudo kill <process id>

# lista di container attivi

sudo docker ps -a

# rimuovi container che usano la stessa porta (5433)

sudo docker rm *nome*

# in alternativa, killa il processo che usa la porta (5433)

sudo docker-compose down  # Stop container on current dir if there is a docker-compose.yml
sudo docker rm -fv $(docker ps -aq)  # Remove all containers

# run container
sudo docker run --name tutorial -p 5433:5432 \
                -e POSTGRES_PASSWORD=mysecretpassword \
                -d postgres

# accedi psql
sudo docker exec -it tutorial psql -U postgres

# in psql
grant usage on schema api to web_anon;
grant all on api.ogginvendita to web_anon;
grant all on api.oggdaconsegn to web_anon;
grant all on api.oggconsegnati to web_anon;

# disabilita postgres on start up

sudo systemctl disable postgresql

# abilita postgres on start up

sudo systemctl enable postgresql

# connect client to server
redis-cli -h 127.0.0.1 -p 6379

# start redis-server
redis-server /etc/redis/redis.conf

# kill redis-server
redis-cli shutdown

ps aux | grep redis
kill -9 *PID*

# start navicat (postgresql GUI) from download directory
chmod +x navicat16-pgsql-en.AppImage
./navicat16-pgsql-en.AppImage
