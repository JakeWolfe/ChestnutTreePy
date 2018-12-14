# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

The Forest class contains state functionality of a MDP.

@author: Quentin Goehrig
"""

from tree import Tree
import config
import sys
import math
from random import random, seed, shuffle
from copy import copy, deepcopy
from datetime import datetime

class Forest:
    
    num_healthy, num_viru, num_hypo, = 0, 0, 0
    # Infect maps to be used for for future work on infect_v2
    # Maps a point -> list of available points
    hv_infect_map = None
    v_infect_map = None
    
    def __init__(self, rows, cols, infect_version = 1, rand_seed = datetime.now()):
        self.rows = rows
        self.cols = cols
        self.infect_version = infect_version
        self.grid = [[None] * cols for i in range(rows)]
        seed(rand_seed)

    # Generates a random Tree grid based on 2002 CDF data
    def set_random_grid(self):
        new_grid = [[None] * self.cols for i in range(self.rows)]
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                rating = 0
                stage = 0
                if random() < config.TREE_DENSITY:
                    i = 0
                    while i <= len(config.POP_2002_CDF):
                        if random() < config.POP_2002_CDF[i]:
                            rating = int(i / config.DBH_STAGE4) + 1
                            stage = int(i % config.DBH_STAGE4) + 1
                            break
                        i += 1
                new_tree = Tree(row, col, rating, stage, config.UNTREATED)
                new_grid[row][col] = new_tree
        self.grid = new_grid
    
    def print_forest(self):
        grid = self.grid
        for row in grid:
            for tree in row:
                print(' '.join([str(tree.stage)]))
                # uncomment below for full tree details
                #tree.print_tree()
        print("---------------------------")
        
    # Returns a 2D list of lists of trees, i.e., the new grid 
    def get_next_year(self):
        prev_year = self.grid
        next_year = deepcopy(self.grid)
                
        coords = [(r,c) for r in range(self.rows) for c in range(self.cols)]
        shuffle(coords)
        
        for coord in coords:
            r = coord[0]
            c = coord[1]
            tree = prev_year[r][c] # original tree
            t_tree = next_year[r][c] # transformed tree
            
            if tree.stage != config.DEAD:
                next_stage_row = int(((tree.rating - 1) * config.DBH_STAGE4)) \
                    + (tree.stage - 1)
                    
                for i in range(0, config.DBH_STAGE4 + 1):
                    if random() < config.NEW_STAGE_CDF[next_stage_row][i]:
                        t_tree.stage = i
                        break
                
                next_rating_row = int(tree.treatment * (config.HEALTHY - 1)) \
                    + (tree.rating - 1)
                
                for i in range(0, config.HEALTHY - 1):
                    if random() < config.NEW_RATING_CDF[next_rating_row][i]:
                        t_tree.rating = i + 1
                        break
                
                if tree.rating == config.V or tree.rating == config.HV:
                    if self.infect_version == 1:
                        self.infect_v1(tree.rating, r, c, prev_year, next_year)
                    elif self.infect_version == 2:
                        self.infect_v2(tree.rating, r, c, prev_year, next_year)
                
                rep = config.REPRODUCTION[tree.rating - 1][tree.stage - 1]
                l = math.exp(-rep)
                p = random()
                rand_poisson = 1
                
                while p > l :
                    p = p * random()
                    rand_poisson += 1
                rand_poisson -= 1
                                    
                sites = copy(coords)
                shuffle(sites)
                while rand_poisson > 0 and len(sites) > 0:
                    site = sites.pop()
                    s_r = site[0]
                    s_c = site[1]
                    if prev_year[s_r][s_c].stage == config.DEAD:
                        next_year[s_r][s_c].stage = config.DBH_STAGE1
                        next_year[s_r][s_c].rating = config.HEALTHY
#                        self.num_births += 1
                        rand_poisson -= 1
        
        return next_year
    
    # State transition
    def set_next_year(self):
        next_year = self.get_next_year()
        self.grid = next_year
        self.update_stats()
    
    """
    The experimental infect function. This is significantly slower than the
    original infect function. This is due to the naive approach the function
    uses to select trees for infection. However, this method incorporates
    distance when selecting a tree. The intention is to provide a higher
    likelyhood of an infection for trees that are closer in distance to the
    source tree while still maintaining expected simulation results.
    """
    def infect_v2(self, r, c, rating, prev_year, next_year):
        max_infections = int(round(math.exp(config.NUM_INF_CDF[0] * random() \
            - config.NUM_INF_CDF[1])))
        events = int(round( random() * max_infections ))
        if events < 1:
            events = 1
        if rating == config.V:
            distribution = config.V_INFECT_RANGE_PROB_8M_INT
        else:
            distribution = config.HV_INFECT_RANGE_PROB_8M_INT
        infections = 0
        sporings = 0
        max_sporings = config.SPORE_SCALAR * events
        while infections < events and sporings < max_sporings:
            if rating == config.HV and random() < config.PER_HV_TO_HV:
                infect_type = config.HV
            else:
                infect_type = config.V
            infect_range = random() * len(distribution) * config.DIST_CLASS
            if infect_range <= config.DIST_CLASS:
                infect_range = config.DIST_CLASS
            attempt_coord = self.get_random_point_at_range(r, c, infect_range)
#            point_dist = self.get_distance(r, c, attempt_coord[0], attempt_coord[1])
#            t1 = int(point_dist / config.DIST_CLASS)
#            t2 = int(infect_range / config.DIST_CLASS)
#            print(infect_range, point_dist)
            land_prob_index = int(infect_range / config.DIST_CLASS)
            spore_land_prob = distribution[land_prob_index]
            attempt_tree = prev_year[attempt_coord[0]][attempt_coord[1]]
            if random() < spore_land_prob and attempt_tree.stage != config.DEAD:
                next_year[attempt_tree.r][attempt_tree.c].rating = infect_type
                infections += 1
            sporings += 1
            
    """
    The original infect function. This is much faster than the newer infect
    function, however, it does not incorporate distance to tree when selecting
    new trees to be infected
    """
    def infect_v1(self, r, c, rating, prev_year, next_year):
        if rating == config.V:
            spore_prob = config.PROB_OF_SPORE_VIRU
        else:
            spore_prob = config.PROB_OF_SPORE_HYPO
        num_infections = 0
        if random() < spore_prob:
            i_power = config.NUM_INF_CDF[0] * random() - config.NUM_INF_CDF[1]
            num_infections = int(round(math.exp(i_power)))
        for i in range(0, num_infections):
            if rating == config.HV and random() < config.PER_HV_TO_HV:
                infect_type = config.HV
                dist_coefficient = config.HV_DIST_OLD
            else:
                infect_type = config.V
                dist_coefficient = config.V_DIST_OLD
            # Calculate distance incrementally for readability
            coefficient_power = dist_coefficient[0] * random() - dist_coefficient[1]
            distance = round(math.exp(coefficient_power) * config.DIST_CLASS)
            distance = int( distance / config.SITE_SIZE )
            
            spore_destination = self.get_random_point_in_range(r, c, distance)
            dest_r = spore_destination[0]
            dest_c = spore_destination[1]
            if self.is_in_grid(dest_r, dest_c):
                next_year[dest_r][dest_c].rating = infect_type
        
    # Returns a tuple coordinate (r', c') of a random point at
    # 'p_range' distance of coordinate (r, c)
    def get_random_point_at_range(self, r, c, p_range):
        p_r = r
        p_c = c
        increment_r = random() < 0.5
        increment_c = random() < 0.5
        distance = sys.float_info.max
        while abs(distance - p_range) > config.SITE_SIZE and distance != 0:
            if random() < 0.5:
                p_r = p_r + 1 if increment_r else p_r - 1
                if not self.is_in_grid(p_r, p_c):
                    p_r = r
                    increment_r = not increment_r
            else:
                p_c = p_c + 1 if increment_c else p_c -1
                if not self.is_in_grid(p_r, p_c):
                    p_c = c
                    increment_c = not increment_c
            distance = self.get_distance(r, c, p_r, p_c)
        return ( p_r, p_c )
    
    # Copied straight from original java program
    # Does not guarantee point is in grid range
    def get_random_point_in_range(self, r, c, p_range):
        if random() < 0.5:
            rand_r = -int((random() * p_range) - 1)
        else:
            rand_r = int((random() * p_range) + 1)
        if random() < 0.5:
            rand_c = -int((random() * p_range) - 1)
        else:
            rand_c = int((random() * p_range) + 1)
        return ( rand_r + r, rand_c + c )
        
    def is_in_grid(self, r, c):
        return r >= 0 and c >= 0 and r < self.rows and c < self.cols

    def get_distance(self, r1, c1, r2, c2):
        return math.sqrt(math.pow((r2 - r1) * config.SITE_SIZE, 2) \
            + math.pow((c2 - c1) * config.SITE_SIZE, 2))
    
    def update_stats(self):
        self.num_healthy, self.num_hypo, self.num_viru = 0, 0, 0
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if self.grid[r][c].rating == config.HEALTHY:
                    self.num_healthy += 1
                elif self.grid[r][c].rating == config.HV:
                    self.num_hypo += 1
                elif self.grid[r][c].rating == config.V:
                    self.num_viru += 1
    
# Testing
#forest = Forest(50,50)
#forest.set_random_grid()
#forest.print_forest()
#for i in range( 0, 10 ):
#    forest.set_next_year()
#    print(i)
#forest.print_forest()
