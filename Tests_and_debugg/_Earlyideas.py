#!/usr/bin/env python3

redis_host = "redis"
stream_key = "skey"
stream2_key = "s2key"
group1 = "grp1"
group2 = "grp2"

import redis
from time import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
r = redis.Redis()

# debug
# print(r.ping())
# print(r.xinfo_stream(stream_key))


   
print( f"stream length before write: {r.xlen( stream_key )}")  

# events are requests made by client io order to buy something
event = {"eventType": "purchase", "amount": 5, "item_id": "XXX"}

#Code for writing a stream directly:
r.xadd(stream_key, event)
print( f"stream length after write: {r.xlen( stream_key )}")

#Code for reading from stream directly:
l = r.xread( count=1, streams={stream_key:0} )
print(l)
print( f"stream length after read: {r.xlen( stream_key )}")

# Get data from read entries
first_stream = l[0]
print( f"got data from stream: {first_stream[0]}")
fs_data = first_stream[1]
for id, value in fs_data:
    print( f"id: {id} value: {value[b'amount']}")
    r.xdel(stream_key, id)

# del all ids entries from the stream
s1 = r.xread( streams={stream_key:0} )
for streams in s1:
    stream_name, messages = streams

    [ r.xdel( stream_name, i[0] ) for i in messages ]


# # possibile formato richiesta ordine
# {
#   "products": [
#     {
#       "productId": 11000,
#       "qty": 2,
#       "productPrice": 3995
#     },
#     {
#       "productId": 11001,
#       "qty": 1,
#       "productPrice": 5450
#     }
#   ]
# }

# # risposta ordine
# {
#   "data": "63f5f8dc3696d145a45775a6", #orderId
#   "error": null
# }