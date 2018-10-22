# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:06:36 2018

A Tree keeps track of all things internal to a tree: (x,y) coordinates,
rating (health), stage (size), and treatment.

@author: Quentin Goehrig
"""

class Tree:
    
    # Jake, I'm leaving the constructor to take in a x, y position as opposed
    # to a Point class for simplicity.
    def __init__(self, x = 0, y = 0, rating = 0, stage = 0, treatment = 0):
        self._x = x
        self._y = y
        self._rating = rating # health
        self._stage = stage # size
        self._treatment = treatment # treatment
        
    #def __eq__(self, other):
        # May need to define custom '==' operator or .equals function
        
    def print_tree(self):
        print( "Tree (" + str(self.x) + ", " + str(self.y) + "):\n  Rating: " +
              str(self.rating) + "\n  Stage: " + str(self.stage) +
              "\n  Treatment: " + str(self.treatment) )
    
    # Property getters, setters. Jake, let me know if I'm being too verbose
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, val):
        self._x = val
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, val):
        self._y = val
        
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, val):
        self._rating = val
        
    @property
    def stage(self):
        return self._stage
    
    @stage.setter
    def stage(self, val):
        self._stage = val
        
    @property
    def treatment(self):
        return self._treatment
    
    @treatment.setter
    def treatment(self, val):
        self._treatment = val
    
# Tests
"""
tree = Tree(0);

tree.x = 1
tree.y = 2
tree.rating = 3

tree.print_tree()
"""