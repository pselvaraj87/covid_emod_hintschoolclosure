# 1) Edit poi_stage1.json to set population size
# 2) Run DTK to generate serialized population
~/DtkTrunk/build/x64/Release/Eradication/Eradication -C poi_stage1.json -P . -I .. -O stage1_5k_output/
# 3) Generate plausible household structure after editing with pop size
./hh_gen_toy.py
# 4) Create new serialpop file based on households
python3 change_ser_pop.py stage1_5k_output/state-00000.dtk
# 5) Add hh props to demog file
python3 add_hh_to_demo.py ../hint_schoolclosure_demographics.json hint_schoolclosure_fromser_toy_demographics.json
# 6) Run DTK
~/DtkTrunk/build/x64/Release/Eradication/Eradication -C poi.json -P . -I . -O sim_toy_1x_output
# 7) Inspect property output
for i in {0..99}; do ./get_infected_by_hh.py sim_toy_1x_output/PropertyReport.json $i | sed 's/, /\n/g'|sed 's/\[//g'|sed 's/\]//g' > data.txt && gnuplot -p -e "plot 'data.txt' with lines"; done 

