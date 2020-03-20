#!/usr/bin/python3 

import json
import sys

pr = json.loads( open( sys.argv[1] ).read() )
total = 0
hh = None
if len( sys.argv ) > 2:
    hh = sys.argv[2]

for thekey in pr["Channels"]:
    if "Statistical Population" in thekey:
        if hh:
            if "Household:" + str( hh ) in thekey:
                #print( pr["Channels"][thekey]["Data"][0] )
                total += pr["Channels"][thekey]["Data"][0]
        else:
            total += pr["Channels"][thekey]["Data"][0]
print( total )


