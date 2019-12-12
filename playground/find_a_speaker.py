#!/usr/bin/python3 -u

import random

speakers = {1: 'Matthias',
            2: 'Markus',
            3: 'Adrian',
            4: 'Susanne',
            5: 'Andi R',
            6: 'Stephan',
            7: 'Thomas'}

print("Speaker: {}".format(speakers[random.randrange(1,len(speakers)+1)]))



