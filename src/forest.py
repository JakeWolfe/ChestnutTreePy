# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

@author: Quentin Goehrig
"""

from tree import Tree
import sys
import math
import config
from random import random, shuffle
from copy import copy, deepcopy

class Forest:
    
    num_deaths, num_births = 0, 0
    
    # TODO: Add getters, setters?
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols for i in range(rows)]
    
    # Generates a random Tree grid based on 2002 CDF data
    def generate_grid(self):
        new_grid = [[None] * self.cols for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                rating = 0 # TODO enum?
                stage = 0
                rand = random()
                if rand < config.TREE_DENSITY:
                    tree_type = random()
                    i = 0
                    while i <= len(config.POP_2002_CDF):
                        if tree_type < config.POP_2002_CDF[i]:
                            rating = int(i / config.DBH_STAGE4) + 1
                            stage = int(i % config.DBH_STAGE4) + 1
                            break
                        i += 1
                new_tree = Tree(row, col, rating, stage, config.UNTREATED)
                new_grid[row][col] = new_tree
        return new_grid
    
    def print_forest(self):
        grid = self.grid
        for row in grid:
            print(' '.join([str(tree.stage) for tree in row]))
            # above only prints stage, uncomment below for full tree details
            # for tree in row
                #tree.print_tree()
        print("---------------------------")
    
    def init_random(self):
        self.grid = self.generate_grid()
        
    # Returns a 2D list of lists of trees, i.e., the new grid 
    # TODO: Add infect function
    def get_next_year(self):
        prev_year = self.grid
        next_year = deepcopy(self.grid)
                
        coords = [(r,c) for r in range(self.rows) for c in range(self.cols)]
        shuffle(coords)
        
        max_infections = 
        
        for coord in coords:
            r = coord[0]
            c = coord[1]
            tree = prev_year[r][c] # original tree
            t_tree = next_year[r][c] # transformed tree
            
            if tree.stage != config.DEAD:
                rand = random()
                next_stage_row = int(((tree.rating - 1) * config.DBH_STAGE4)) \
                    + (tree.stage - 1)
                    
                for i in range(0, config.DBH_STAGE4 + 1):
                    if rand < config.NEW_STAGE_CDF[next_stage_row][i]:
                        t_tree.stage = i
                        break
                
                rand = random()
                next_rating_row = int(tree.treatment * (config.HEALTHY - 1)) \
                    + (tree.rating - 1)
                
                for i in range(0, config.HEALTHY - 1):
                    if rand < config.NEW_RATING_CDF[next_rating_row][i]:
                        t_tree.rating = i + 1
                        break
                
                if tree.rating == config.V or tree.rating == config.HV:
                    self.infect(tree.rating, r, c, prev_year, next_year)
                
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
                        self.num_births += 1
                        rand_poisson -= 1
        
        return next_year
    
#    Prelim    
    def infect(self, r, c, rating, prev_year, next_year):
        max_infections = round(math.exp(config.NUM_INF_CDF[0] * random() \
            - config.NUM_INF_CDF[1]))
        events = round( random() * max_infections )
        if events < 1:
            events = 1
        if rating == config.V:
            distribution = config.V_INFECT_RANGE_PROB_8M_INT
        else:
            distribution = config.HV_INFECT_RANGE_PROB_8M_INT
        infections = 0
        sporings = 0
#        print("events", events)
#        print("infections", infections)
        while infections < events and sporings < config.SPORE_SCALAR * events:
            if rating == config.HV and random() < config.PER_HV_TO_HV:
                infect_type = config.HV
            else:
                infect_type = config.V
            infect_range = random() * len(distribution) * config.DIST_CLASS
            if infect_range <= config.DIST_CLASS:
                infect_range = config.DIST_CLASS
            attempt_coord = self.get_random_point(r, c, infect_range)
            point_dist = self.get_distance(r, c, attempt_coord[0], attempt_coord[1])
            spore_land_prob = distribution[0]
            land_prob_index = int(point_dist / config.DIST_CLASS)
            spore_land_prob = distribution[land_prob_index]
#            while i < len(distribution):
#                if point_dist < (i * config.DIST_CLASS):
#                    spore_land_prob = distribution[i] - distribution[i - 1]
#                i += 1
            attempt_tree = prev_year[attempt_coord[0]][attempt_coord[1]]
            if random() < spore_land_prob and attempt_tree.stage != config.DEAD:
                next_year[attempt_tree.r][attempt_tree.c].rating = infect_type
                infections += 1
            sporings += 1

    
    # Returns a tuple coordinate (r', c') of a random point at
    # 'range' distance of coordinate (r, c)
    def get_random_point(self, r, c, p_range):
        p_r = r
        p_c = c
        increment_r = random() < 0.5
        increment_c = random() < 0.5
        distance = sys.float_info.max
        while abs(distance - p_range) > config.SITE_SIZE and distance > 0:
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



    def is_in_grid(self, r, c):
        return r >= 0 and c >= 0 and r < self.rows and c < self.cols

    def get_distance(self, r1, c1, r2, c2):
        return math.sqrt(math.pow(abs(r2 - r1) * config.SITE_SIZE, 2) \
            + math.pow(abs(c2 - c1) * config.SITE_SIZE, 2))

    # Generates a new grid for the Forest and sets the active grid to
    # the grid of the next year
    def set_next_year(self):
        next_year = self.get_next_year()
        self.grid = next_year

            
                
# Testing
#forest = Forest(50,50)
#forest.grid = forest.generate_grid() # maybe initialize on new grid?
#forest.print_forest()
#for i in range( 0, 20 ):
#    forest.set_next_year()
#    print(i)
#forest.print_forest()
