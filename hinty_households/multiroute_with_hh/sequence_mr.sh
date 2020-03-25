#!/usr/bin/bash

# OK, the idea here is to get around the seeming bug (at least crash) after starting up from the modified serialized population.
# Take the two steps of creating the synthetic households and do them separately. The first step is the modification of the 
# serialized population to assigned people to households as desired. The second step is modifying the demographics file
# to include the possible household ips. 
# Let's take the new demographics file and create a new serialized population file from that. The assignments to household
# will be wrong, but the household labels themselves will be right.
# In this step we don't do the modification of the serialized population file yet. We just show taht we can serialized
# and deserialize.
~/EMOD/DtkTrunk-GO/build/x64/Release/Eradication/Eradication -C poi_stage1_hh.json -P . -I . -O stage1_1k_mr_hh_output
#python3 change_ser_pop.py stage1_hh_1k_mr_output/state-00000.dtk
~/EMOD/DtkTrunk-GO/build/x64/Release/Eradication/Eradication -C poi_nomods.json -P . -I . -O sim_1k_mr_output
