#!/usr/bin/python

import regression_utils as ru
#import dtk_utils.regression as config
import os

def application( json_config_path ):
    new_config_filename = "config.json"
    ru.flattenConfig( json_config_path, new_config_filename  )
    return new_config_filename 
