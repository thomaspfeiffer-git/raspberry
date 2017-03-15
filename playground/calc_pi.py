#!/usr/bin/python3
###############################################################################
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################

import concurrent.futures
from datetime import datetime
import math
import multiprocessing
from random import random

iterations = 100000000000

def calc ():
    r = {False: 0, True: 0}
    for i in range(iterations):
        r[math.sqrt(random()**2.0 + random()**2.0) <= 1.0] += 1
    return r

print(datetime.now())

workers = multiprocessing.cpu_count()
results = [None for i in range(workers)]                               
with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as e:       
    for i in range(workers):       
        results[i] = e.submit(calc)       
                                   
a = sum(results[i].result()[True] for i in range(len(results)))
b = sum(results[i].result()[False] for i in range(len(results)))
                                                        
mypi = 4.0*a/(iterations*workers)                          
print("mypi: {:.50f}".format(mypi))  
print("deviation: {:2.10f} %".format((math.pi-mypi)/math.pi*100.0))
                                                              
print(datetime.now())

# eof #                                                       

