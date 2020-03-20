#!/usr/bin/python3 

import json
import sys
import pdb

pr = json.loads( open( sys.argv[1] ).read() )
infecteds = []
hh = None
if len( sys.argv ) > 2:
    hh = sys.argv[2]

for thekey in pr["Channels"]:
    if "Infected" in thekey:
        if hh:
            if thekey.endswith( "Household:" + str( hh ) ):
                #print( thekey + "..." + str( pr["Channels"][thekey]["Data"] ) + "..." + str( len(pr["Channels"][thekey]["Data"]) ) )
                if len(infecteds) == 0:
                    infecteds = pr["Channels"][thekey]["Data"]
                    #print( infecteds )

                else:
                    for tstep in range(len(pr["Channels"][thekey]["Data"])):
                        infecteds[tstep] += pr["Channels"][thekey]["Data"][tstep]
                    #print( infecteds )
        else:
            total += pr["Channels"][thekey]["Data"][0]
#pdb.set_trace()
print( infecteds )


