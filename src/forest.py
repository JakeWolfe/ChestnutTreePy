# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

@author: Quentin Goehrig
"""

from tree import Tree
import random
import config

class Forest:
    
    # TODO: Add getters, setters
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols for i in range(rows)]
    
    def get_next_year(self):
        new_grid = [[None] * self.cols for i in range(self.rows)]
        return new_grid
    
    # Generates a random Tree grid based on 2002 CDF data
    def generate_grid(self):
        new_grid = [[None] * self.cols for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                rating = 0 # TODO enum
                stage = 0
                rand = random.random()
                if rand < config.TREE_DENSITY:
                    tree_type = random.random()
                    i = 0
                    while i <= len(config.POP_2002_CDF):
                        if tree_type < config.POP_2002_CDF[i]:
                            rating = i / config.DBH_STAGE4 + 1
                            stage = i % config.DBH_STAGE4 + 1
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

# Testing
test_forest = Forest(50,50)
test_forest.grid = test_forest.generate_grid()
test_forest.print_forest()
    

