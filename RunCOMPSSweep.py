##
"""
Measles Ward Simulations: Sample demographic
"""
#
import os
import sys
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from simtools.SetupParser import SetupParser
from simtools.ModBuilder import ModBuilder, ModFn
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from dtk.utils.Campaign.CampaignClass import *
from dtk.tools.demographics.Node import Node
from dtk.tools.demographics.DemographicsFile import DemographicsFile
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Analysis.BaseAnalyzers import DownloadAnalyzer
from simtools.Utilities.COMPSUtilities import get_experiment_by_id
from COMPS.Data import QueryCriteria
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PythonHelperFunctions.DemographicsHelpers import *
from PythonHelperFunctions.utils import load_dropbox_path
from pyDOE import lhs
import numpy as np

#Run locally or on HPC
SetupParser.default_block = "HPC"
SetupParser.init(selected_block=SetupParser.default_block)


# Set the path for DTK input files
DTKFileInputPath = 'BaseInputFiles'
if not os.path.exists(DTKFileInputPath):
    os.mkdir(DTKFileInputPath)
DTKFileOutputPath = 'test'
if not os.path.exists(DTKFileOutputPath):
    os.mkdir(DTKFileOutputPath)
outputPath = 'COMPS_outputs'
if not os.path.exists(outputPath):
    os.mkdir(outputPath)

#Name the input files
DemoFile = os.path.join(DTKFileInputPath, 'demographics.json')
CampaignFile = os.path.join(DTKFileInputPath, 'campaign.json')
ConfigFile = os.path.join(DTKFileInputPath, 'config.json')


SimDurationInYears = 1
TotalPopulation = 3e6
cb = DTKConfigBuilder.from_files(ConfigFile, campaign_name=CampaignFile)
cb.set_param('Simulation_Duration', SimDurationInYears*365.0)


demoFile = DemographicsFile.from_file(DemoFile)
demoFile.content['Nodes'][0]['NodeAttributes']['InitialPopulation'] = TotalPopulation
demoFile = SetAgeDistribution(demoFile, os.path.join(load_dropbox_path(),
                'COVID-19','seattle_network','census','age distributions', 'puma_age_dists.csv'))

TotalTransmissionMatrix = TranmissionMatrixFromAgeContactMatrix(filename = os.path.join(load_dropbox_path(),
                'COVID-19','age_contact_matrices', 'MUestimates_all_locations_2.xlsx'))
SchoolTransmissionMatrix = TranmissionMatrixFromAgeContactMatrix(filename = os.path.join(load_dropbox_path(),
                'COVID-19','age_contact_matrices', 'MUestimates_school_2.xlsx'))
HomeTransmissionMatrix = TranmissionMatrixFromAgeContactMatrix(filename = os.path.join(load_dropbox_path(),
                'COVID-19','age_contact_matrices', 'MUestimates_home_2.xlsx'))
WorkTransmissionMatrix = TranmissionMatrixFromAgeContactMatrix(filename = os.path.join(load_dropbox_path(),
                'COVID-19','age_contact_matrices', 'MUestimates_work_2.xlsx'))



demoFile = SetPropertyDependentTransmission(demoFile, TransmissionMatrix_pre=TotalTransmissionMatrix,
                                            TransmissionMatrix_post=TotalTransmissionMatrix-SchoolTransmissionMatrix,
                                            Time_start=40, Duration=2000)  #Set up a bunch of default properties.

demoFile.generate_file(DTKFileOutputPath)
cb.set_param("Demographics_Filenames", [os.path.basename(DemoFile)])

#Add all of the necessary experiment files
cb.set_experiment_executable(path=os.path.join('Executable', 'Eradication.exe'))
cb.set_input_files_root(DTKFileOutputPath)
cb.set_dll_root(DTKFileOutputPath)

#Define a sample point function for doing sweeps/sampling.  This function basically maps the sampled parameters, fed
# as a dictionary, to the configuration and campaign parameters that should be changed.
def sample_point_fn(CB, params_dict, sample_index):
    tags ={}

    for param, value in params_dict.items():
        if param.startswith('META'):
            None

        else:
            CB.set_param(param, value)
            tags[param] = value
    tags['__sample_index__']=sample_index
    return tags



if __name__ == "__main__":

    #A dictionary of parameters to sample, and the range to sample from
    sample_dimension_dict = {}
    sample_dimension_dict['Base_Infectivity'] = [0.125, 4.0]

    #Doing a parameter sweep uses a list of abstract functions, here contained in mod_fns.  These functions basically
    #change values in the "cb" object that contains the config and campaign files, as a dict and a class, respectively.
    mod_fns = []
    random.seed(12884)
    nSamples = 1
    LHSsamps = lhs(len(sample_dimension_dict), samples=nSamples)

    for ix in range(nSamples):
        param_dict = {}
        currDim = 0
        for param, paramRange in sample_dimension_dict.items():
            param_dict[param] = paramRange[0] + (paramRange[1]-paramRange[0])*LHSsamps[ix][currDim]
            currDim += 1
        mod_fns.append(ModFn(sample_point_fn, param_dict, ix))

    builder = ModBuilder.from_combos(mod_fns)

    exp_name = 'Simple Sweep sampling over R0'
    exp_manager = ExperimentManagerFactory.from_cb(cb)

    run_sim_args = {'config_builder': cb,
                    'exp_name': exp_name,
                    'exp_builder': builder}

    exp_manager.run_simulations(**run_sim_args)
    time.sleep(5)
    exp_manager.wait_for_finished(verbose=True)
    am = AnalyzeManager('latest', analyzers=DownloadAnalyzer(filenames=['output/InsetChart.json'], output_path=outputPath))
    am.analyze()
