# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some
m x n grid under some predefined biological-enviornment parameters.

@author: Quentin Goehrig
"""

from tree import Tree

class Forest:
    
    # TODO: Add getters, setters
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols for i in range(rows)]
    
    def get_next_year(self):
        new_grid = [[None] * self.rows for i in range(self.cols)]
        return new_grid


# Should be a class definition, just used for testing right now
def init_forest(forest):
    grid = forest.grid
    for i in range(forest.rows):
        for j in range(forest.cols):
            grid[i][j] = Tree(i, j)
            
    for row in grid:
        print(' '.join([str(elem.x) for elem in row]))


forest = Forest(10,5)
init_forest(forest)
    

