#!/usr/bin/python3

import json
import sys

if len( sys.argv ) < 3:
    print( f"Usage: {sys.argv[0]} <input_demog_file.json> <output_demog_file.json>" )
    sys.exit()

demog_json = json.loads( open( sys.argv[1] ).read() )

# TBD: Get the list of household ids from the previous script
hh_ids = json.loads( open( "household_ids.json" ).read() )
num_hhs = len(hh_ids) # should be 25, hunt down off-by-1 error

INTRA_HH_MULT = 1.0
INTER_HH_MULT = 0.1

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
    hh_prop[ "Initial_Distribution" ].append( 0 )
hh_prop[ "Initial_Distribution" ][0] = 1.0 # not this is nonsense but irrlevantly so for us.

# OK, now create the matrix. num_hhsxnum_hhs with 1.0's on diagonal
for row in range(num_hhs):
    hh_prop[ "TransmissionMatrix" ][ "Matrix" ].append( list )
    hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row] = []
    for col in range(num_hhs):
        if row == col:
            hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row].append( INTRA_HH_MULT )
        else:
            hh_prop[ "TransmissionMatrix" ][ "Matrix" ][row].append( INTER_HH_MULT  )


demog_json[ "Defaults" ][ "IndividualProperties" ].append( hh_prop )

with open( sys.argv[2],"w+" ) as outfile:
    json.dump( demog_json, outfile, sort_keys=True, indent=4 )
