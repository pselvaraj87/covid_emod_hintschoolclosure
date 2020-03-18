# HINT-based Households

This is a work-in-progress for collaboration and review.

The idea here is to use the IDM EMOD HINT feature to model households. We run a single timestep simulation with an age-based Individual Property and HINT setup and then serialize the population.

We then use a python script to load this .dtk file as json, and adding a Household IP to each individual with a value to represent their household. In the proof-of-concept version, the households are random. In the second version, the households are taken from a json file that is created by a standalone hh creation script designed to create "plausible" households. In the third version Research uses actual household data files.

The python script that manipulates the serialized pop file saves a new file with the HH IPs. This then is used as an input to the DTK. There is a third Python script that takes the demographics.json file and adds a Household IP and Transmission Matrix. The output of this is used as the actual demographics.json for the subsequent simulation.

To take .dtk file from DTK run and add household IPs:

```
python3 change_ser_pop.py ../output/state-00000.dtk
```

New file is written to:

my_sp_file.dtk

To add households to new demographics file (so modified serialized population will be accepted and to have HH tx matrix):

```
python3 add_hh_to_demo.py <orig_demog.json> <new_demog.json>

```

Make sure the number of households matches.


Run DTK a la:

~/DtkTrunk/build/x64/Release/Eradication/Eradication -C config_fromser.json 

Note: by dialing hh's down to 25, I did get some transmission.

Will keep working on this. PropertyReport will be useful here but probably not visually -- too many plots.
