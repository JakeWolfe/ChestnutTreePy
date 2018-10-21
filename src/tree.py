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
    def __init__(self, x, y, rating, stage, treatment):
        self._x = x
        self._y = y
        self._rating = rating # health
        self._stage = stage # size
        self._treatment = treatment # treatment
        
    #def __eq__(self, other):
        # May need to define custom '==' operator or .equals function
    
    @property
    def x(self):
        """ Gets the '_x' property """
        return self._x
    
    @property
    def x.setter(self, x):
        """ Sets the '_x' property """
        return self._x = x
        
    def print_tree(self):
        print( "Tree (" + str(self.x) + ", " + str(self.y) + "):\n  Rating: " +
              str(self.rating) + "\n  Stage: " + str(self.stage) +
              "\n  Treatment: " + str(self.treatment) )
    
     
test1 = Tree(1,1,2,3,4);
test2 = Tree(1,1,2,3,4);

test1.print_tree()