# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:06:36 2018

A Tree keeps track of all things internal to a tree: (x,y) coordinates,
rating (health), stage (size), and treatment.

@author: Quentin Goehrig
"""

class Tree:
    
    def __init__(self, r = 0, c = 0, rating = 0, stage = 0, treatment = 0):
        self._r = r # row
        self._c = c
        self._rating = rating # health
        self._stage = stage # size
        self._treatment = treatment # treatment
        
    #def __eq__(self, other):
        # May need to define custom '==' operator or .equals function
        
    def print_tree(self):
        print( "Tree (" + str(self.r) + ", " + str(self.c) + "):\n  Rating: " +
              str(self.rating) + "\n  Stage: " + str(self.stage) +
              "\n  Treatment: " + str(self.treatment) )
    
    # r: row of tree
    @property
    def r(self):
        return self._r
    
    @r.setter
    def r(self, val):
        self._r = val
    
    # c: column of tree
    @property
    def c(self):
        return self._c
    
    @c.setter
    def c(self, val):
        self._c = val
    
    # rating: health of tree ( V, HV, Healthy )
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, val):
        self._rating = val
    
    # rating: health of tree ( V, HV, Healthy )
    @property
    def stage(self):
        return self._stage
    
    # stage: Size of tree, 0 = dead, 1-4 see DBH_STAGEs
    @stage.setter
    def stage(self, val):
        self._stage = val
        
    # treatment: 0 = untreated, 1 = treated
    @property
    def treatment(self):
        return self._treatment
    
    @treatment.setter
    def treatment(self, val):
        self._treatment = val
    