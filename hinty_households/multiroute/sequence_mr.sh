#!/usr/bin/bash

~/EMOD/DtkTrunk-GO/build/x64/Release/Eradication/Eradication -C poi_stage1.json -P . -I . -O stage1_1k_mr_output
python3 change_ser_pop.py stage1_1k_mr_output/state-00000.dtk
~/EMOD/DtkTrunk-GO/build/x64/Release/Eradication/Eradication -C poi_nomods.json -P . -I . -O sim_1k_mr_output
