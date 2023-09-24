# old redis-server  (using redis labs for testing)

# REDIS_HOSTNAME="redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com"
# REDIS_PORT="17843"
# REDIS_PASSWORD="meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh"

# redis-cli -h redis-17843.c55.eu-central-1-1.ec2.cloud.redislabs.com -p 17843 -a meEXVH7HGCyWaXh0qCYpaiH2MqCDZIqh


# redis-server (lato cliente)

REDIS_HOSTNAME_S1="192.168.1.70"
REDIS_PORT_S1="6379"
REDIS_PASSWORD_S1="mnbdZrOrdM29eX/G7ySceE8pEnFp4rlCP7N3/k80MB3kAQURiSy0wnRDgHLUfF0TvNPRPu4/0IRX9qGx"

# redis-server2 (lato trasportatore)
REDIS_HOSTNAME_S2="192.168.1.70"
REDIS_PORT_S2="6380"
REDIS_PASSWORD_S2="mnbdZrOrdM29eX/G7ySceE8pEnFp4rlCP7N3/k80MB3kAQURiSy0wnRDgHLUfF0TvNPRPu4/0IRX9qGx"

# redis-server3 (lato fornitore)
REDIS_HOSTNAME_S3="192.168.1.70"
REDIS_PORT_S3="6381"
REDIS_PASSWORD_S3="mnbdZrOrdM29eX/G7ySceE8pEnFp4rlCP7N3/k80MB3kAQURiSy0wnRDgHLUfF0TvNPRPu4/0IRX9qGx"

# redis-cli -h 192.168.1.70 -p 6379 -a mnbdZrOrdM29eX/G7ySceE8pEnFp4rlCP7N3/k80MB3kAQURiSy0wnRDgHLUfF0TvNPRPu4/0IRX9qGx

#include "../MyOtherConfigFile.xcconfig"    

# useful commands:

# get public ip (192.168.1.70) # my public
# hostname -I

# connect remotely test
# redis-cli -h public host ip -p port -a password 
# es. redis-cli -h 192.168.1.70 -p 6379 -a mnbdZrOrdM29eX/G7ySceE8pEnFp4rlCP7N3/k80MB3kAQURiSy0wnRDgHLUfF0TvNPRPu4/0IRX9qGx (per serverCliente)

