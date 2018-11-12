# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

@author: Quentin Goehrig
"""

from tree import Tree
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
                
                # block not required?
                if tree.stage == config.DEAD:
                    t_tree.stage = config.DEAD
                    t_tree.treatment = config.UNTREATED
                    
                    # TODO: decide if reset tree treatment here
                else:
                    rand = random()
                    next_rating_row = int(tree.treatment * (config.HEALTHY - 1)) \
                        + (tree.rating - 1)
                    
                    for i in range(0, config.HEALTHY - 1):
                        if rand < config.NEW_RATING_CDF[next_rating_row][i]:
                            t_tree.rating = i + 1
                            break
                    
                    #if tree.rating == config.V:
                        #infect(config.V, r, c, prev_year, next_year)
                    #else if tree.rating == config.HV
                        #infect(config.HV, ...)
                    
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
    def infect(self):
        maxInfections = 3
        events = math.round( random() * maxInfections )
        if events < 1:
            events = 1
        if treeType == config.V:
            distribution = config.V_INFECT_RANGE_PROB_8M_INT
        else:
            distribution = config.V_INFECT_RANGE_PROB_8M_INT
        infections = 0
        sporings = 0

    # Generates a new grid for the Forest and sets the active grid to
    # the grid of the next year
    def set_next_year(self):
        next_year = self.get_next_year()
        self.grid = next_year

            
                
# Testing
forest = Forest(4,16)
forest.grid = forest.generate_grid() # maybe initialize on new grid?
forest.print_forest()
for i in range( 0, 20 ):
    forest.set_next_year()
forest.print_forest()
