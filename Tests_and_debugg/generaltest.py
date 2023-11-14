import time
import datetime
from timeit import default_timer as timer
import random

myseed = datetime.datetime.now().timestamp()
print(myseed) 
random.seed(myseed) # set the seed for the run

