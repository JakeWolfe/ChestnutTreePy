# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 20:00:35 2018

Simulation control for the spread of Chestnut Blight.
Adds actions to the MDP.
Contains data recording functionality.

@author: Quentin Goehrig
"""

import csv
import time
from forest import Forest

class DataRecorder:
    
    def __init__(self, forest, treat50 = False, record_stats = False):
        self.forest = forest
        self.treat50 = treat50
        self.record_stats = record_stats
    
#    def create_csv_statfile(self):

    def record_data(self, runs, years):
        timestamp = time.strftime("%Y-%m-%d-%H%M")
        name = "BlightStats-" + timestamp
        with open(name, mode='w') as csv_file:
            fieldnames = ['run', 'year', 'num_healthy', 'num_viru', 'num_hypo']
            writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            writer.writeheader()
            
            for run in range(0, runs):
                self.forest.set_random_grid()
                for year in range(0, years):
                    healthy = self.forest.num_healthy
                    viru = self.forest.num_viru
                    hypo = self.forest.num_hypo
                    writer.writerow({'run': run, 'year': year, 'num_healthy': \
                        healthy, 'num_viru': viru, 'num_hypo': hypo })
                    self.forest.set_next_year()                    
                    

# TODO: command line args
forest = Forest(50, 50)
recorder = DataRecorder(forest, False, True)
recorder.record_data(10, 10)
