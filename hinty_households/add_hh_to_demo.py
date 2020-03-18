#!/usr/bin/python3

import json
import sys

demog_json = json.loads( open( sys.argv[1] ).read() )
print( demog_json[ "Defaults" ][ "IndividualProperties" ][1] )

num_hhs = 501

hh_prop = {}
hh_prop[ "Property" ] = "Household"
hh_prop[ "Values" ] = []
hh_prop[ "Initial_Distribution" ] = []
hh_prop[ "Transitions" ] = []
hh_prop[ "TransmissionMatrix" ] = {}
hh_prop[ "TransmissionMatrix" ][ "Route" ] = "Contact"
hh_prop[ "TransmissionMatrix" ][ "Matrix" ] = []

for hh_id in range( num_hhs ):
    hh_prop[ "Values" ].append( str( hh_id ) )
    hh_prop[ "Initial_Distribution" ].append( 1.0/num_hhs )

# OK, now create the matrix. num_hhsxnum_hhs with 1.0's on diagonal
for row in range(num_hhs):
    hh_prop[ "TransmissionMatrix" ][ "Matrix" ].append( list )
    hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row] = []
    for col in range(num_hhs):
        if row == col:
            hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row].append( 1 )
        else:
            hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row].append( 0 )
        #hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row][col] = 0


demog_json[ "Defaults" ][ "IndividualProperties" ][1] = hh_prop

with open( sys.argv[2],"w+" ) as outfile:
    json.dump( demog_json, outfile, sort_keys=True, indent=4 )
