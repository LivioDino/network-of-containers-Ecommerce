# FROM redis
# COPY redis.conf /usr/local/etc/redis/redis.conf
# CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]


# FROM redis
# COPY redis3.conf /etc/redis/redis3.conf
# CMD [ "sudo systemctl start redis-server3.service" ]


# COPY . /usr/app

# WORKDIR /usr/app/

# EXPOSE 6379

# CMD redis-server --protected-mode no

FROM redis
CMD [ "sudo systemctl start redis-server.service" ]