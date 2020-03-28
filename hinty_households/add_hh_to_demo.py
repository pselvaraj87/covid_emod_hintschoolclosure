#!/usr/bin/python3

import json
import sys

if len( sys.argv ) < 3:
    print( f"Usage: {sys.argv[0]} <input_demog_file.json> <output_demog_file.json>" )
    sys.exit()

demog_json = json.loads( open( sys.argv[1] ).read() )

# TBD: Get the list of household ids from the previous script


INTRA_HH_MULT = 10.0
INTER_HH_MULT = 0.0

def get_props( route, ip_key, num_ids ):
    hh_prop = {}
    hh_prop[ "Property" ] = ip_key
    hh_prop[ "Values" ] = []
    hh_prop[ "Initial_Distribution" ] = []
    hh_prop[ "Transitions" ] = []
    hh_prop[ "TransmissionMatrix" ] = {}
    hh_prop[ "TransmissionMatrix" ][ route ] = {}
    hh_prop[ "TransmissionMatrix" ][ route ][ "Matrix" ] = []

    for hh_id in range( num_ids ):
        hh_prop[ "Values" ].append( str( hh_id ) )
        hh_prop[ "Initial_Distribution" ].append( 0 )
    hh_prop[ "Initial_Distribution" ][0] = 1.0 # not this is nonsense but irrlevantly so for us.

# OK, now create the matrix. num_idsxnum_ids with 1.0's on diagonal
    for row in range(num_ids):
        hh_prop[ "TransmissionMatrix" ][ route ][ "Matrix" ].append( list )
        hh_prop[ "TransmissionMatrix" ][ route ][ "Matrix" ][row] = []
        for col in range(num_ids):
            if row == col:
                hh_prop[ "TransmissionMatrix" ][ route ][ "Matrix" ][row].append( INTRA_HH_MULT )
            else:
                hh_prop[ "TransmissionMatrix" ][ route ][ "Matrix" ][row].append( INTER_HH_MULT  )
    return hh_prop


#demog_json[ "Defaults" ][ "IndividualProperties" ].append( hh_prop )
primary_ids = json.loads( open( "primary_ids.json" ).read() )
num_primaries = max(primary_ids)+3
print( "No. Primaries = " + str( num_primaries ) )
demog_json[ "Defaults" ][ "IndividualProperties" ][0] = get_props( "contact", "Primary", num_primaries )

hh_ids = json.loads( open( "household_ids.json" ).read() )
num_hhs = len(hh_ids) # should be 25, hunt down off-by-1 error
print( "No. Households = " + str( num_hhs ) )
if len(demog_json[ "Defaults" ][ "IndividualProperties" ] ) == 1:
    demog_json[ "Defaults" ][ "IndividualProperties" ].append( get_props( "environmental", "Household", num_hhs ) )
else:
    demog_json[ "Defaults" ][ "IndividualProperties" ][1] = get_props( "environmental", "Household", num_hhs )


with open( sys.argv[2],"w+" ) as outfile:
    json.dump( demog_json, outfile, sort_keys=True, indent=4 )
