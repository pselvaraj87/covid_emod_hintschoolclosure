#!/usr/bin/python
import json
import numpy as np
import pdb
import random
import sys # ArgParse is too heavy

"""
S=Senior (actually not yet)
W=Working Age Adult
C=Adult in Community (e.g.,SAHM) or baby
HS=High School
JH=Junior High
ES=Elem School

Nothing for daycare or college in this toy example

Create a bunch of households with increasing idsfrom 000 up to 10k total people.

size of hh is exponential, at least 1, mean = 3. (why not?)

Always start with adult.

If need another person:
    50% prob adult, 50% prob not
    pick between 
"""

second_random = { 0: "W", 1: "C", 2: "HS", 3: "JH", 4: "ES" }
child_random = { 0: "C", 1: "ES", 2: "JH", 3: "ES"  }

hhs = {}
person_id = 0
hh_id = 0
pop = int(sys.argv[1]) if len(sys.argv)>=1 else 1000
while person_id < pop:
    hhs[hh_id] = [] # insert elem into dict for all members of this household
    hh_size = int(np.random.exponential(2)+1)
    #pdb.set_trace()
    for member in range(hh_size):
        if member == 0:
            # pick an adult
            hhs[hh_id].append( "W" )
        elif member == 1:
            hhs[hh_id].append( second_random[ random.randint( 0,4 ) ] )
        else:
            hhs[hh_id].append( child_random[ random.randint( 0,3 ) ] )
            # 33% W, C, or student
        person_id += 1
    hh_id += 1

print( json.dumps( hhs ) )
with open( "households.json", "w+" ) as hh_file:
    json.dump( hhs, hh_file, sort_keys=True, indent=4 )
