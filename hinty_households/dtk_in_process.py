#!/usr/bin/python

import json
import sqlite3
import pdb
import math

def application( timestep ):
    # Do SQL query against simulation.db (?) and look for any NewlySymptomatic events this timestep
    # If there are any, for each individual, do a query for any NewInfection events within last 5 days
    # where the infector id == the id of the newly symptomatic individual.
    # Create a new campaign file which distributes SimpleVaccine to those individuals.
    # This will require creation of new method to target interventions by individual id


    # CREATE TABLE SIM_EVENTS (SIM_TIME       INT    NOT NULL,EVENT          TEXT     NOT NULL,INDIVIDUAL     INT    NOT NULL,MISC           INT    NOT NULL);

    no_op = True

    timestep = int(float(timestep))-1
    newly_symptos = []
    victims_to_treat = []
    with sqlite3.connect('simulation_events.db') as conn:
        cur = conn.cursor()
        query = "SELECT INDIVIDUAL from SIM_EVENTS where SIM_TIME=={} and EVENT=='NewlySymptomatic';".format( timestep ) 
        cur.execute( query )
        rows = cur.fetchall()
        for row in rows:
            infector = row[0]
            #print( f"Found newly symptomatic individual {infector}. Look for victims..." )
            newly_symptos.append( infector )

        for infector in newly_symptos:
            #print( "Looking for victims of {}".format( infector ) )
            cur2 = conn.cursor()
            query2 = "SELECT INDIVIDUAL from SIM_EVENTS where SIM_TIME<={} and SIM_TIME>{} and EVENT=='NewInfection' and MISC=={};".format( timestep, timestep-20, infector )
            cur2.execute( query2 )
            rows2 = cur2.fetchall()
            for row in rows2:
                #print( str( row ) )
                infected = row[0]
                #print( f"Found infected victim {infected} of {infector}." )
                victims_to_treat.append( infected )

    if len(victims_to_treat ) > 0:
        print( "Going to distribute vaccines to {}.".format( victims_to_treat ) )
        no_op = False

    if no_op:
        return ""

    campaign = {}
    campaign["Events"] = []
    event = {}
    event = json.loads(
        """
        {
            "Start_Day": 0,
            "class": "CampaignEvent",
            "Event_Coordinator_Config": {
                "Intervention_Config": {
                "class": "SimpleVaccine",
                    "Vaccine_Type": "TransmissionBlocking",
                    "Waning_Config": {
                        "class": "WaningEffectBox",
                        "Initial_Effect": 0.5,
                        "Box_Duration": 30
                    }
                },
                "Target_Demographic": "ExplicitIDs",
                "ID_List": [],
                "class": "StandardInterventionDistributionEventCoordinator"
            },
            "Nodeset_Config": {
                "class": "NodeSetAll"
            }
        }
        """
    )
    event["Start_Day"] = float(timestep+1)
    event["Event_Coordinator_Config"]["Intervention_Config"]["ID_List"] = victims_to_treat
    campaign["Events"].append( event )
    with open( "contact_trace.json", "w" ) as camp_file:
        json.dump( campaign, camp_file )
    return "contact_trace.json" 

