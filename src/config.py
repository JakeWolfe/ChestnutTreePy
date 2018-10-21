"""
Description: Global Variables used for problem specifications.

Author: Jake Wolfe
"""
import math

"""
-------------------------------------------------------
                 SIMULATION SETTINGS 
-------------------------------------------------------
""" 
# Number of years for simulating, classifier training
YEARS = 200

# Size of a square within the world (2x2 meters)
SITE_SIZE = 2

# Scalar value used to determine infection range distance of a tree (meters)
DIST_CLASS = 8

# Used to calculate the number of infection "attempts" when determining which 
# trees will get infected. This new value was introduced when modifying the 
# infection algorithm to change some unintended behavior. The old method would 
# calculate the number of trees to be infected within a certain distance and then 
# infect them at random. This method did not take tree spacial locality into 
# consideration when selecting a new tree to infect. Instead, the infected tree 
# now selectes tiles at random, favoring those tiles closer to the source tree, 
# given a number of sporing events. The current infection still mimics the 
# anticipated West Salem data in the # of infections, but now takes more 
# consideration to tree locality. The downside to this is that the simulation 
# time increases.
SPORE_SCALAR = 400

# Forest height (SITESIZE tiles)
HEIGHT = 50

# Forest width (SITESIZE tiles)
WIDTH = 50

"""
-------------------------------------------------------
                 TREE STATE DEFINITIONS 
-------------------------------------------------------
""" 
# Titled a Simulation "Action", but really is a treatment STATE
UNTREATED = 0

# Titled a Simulation "Action", but really is a treatment STATE
TREATED = 1

# Virulent - A tree health rating. All virulent cankers 
V = 1

# Hypovirulent - A tree health rating. Mix of virulent and hypovirulent cankers
HV = 2

# Healthy - A tree health rating.
HEALTHY = 3

# DBH Stage - Indicates a dead tree. (Diameter at Breast Height)
DEAD = 0

# DBH Stage - DBH <= 1 cm
DBH_STAGE1 = 1

# DBH Stage -  1 < DBH <= 10 cm
DBH_STAGE2 = 2

# DBH Stage -  10 < DBH <= 20 cm
DBH_STAGE3 = 3

# DBH Stage -  DBH > 20 cm
DBH_STAGE4 = 4


"""
-------------------------------------------------------
              GROWTH / INFECTION MATH 
-------------------------------------------------------
""" 
# From rough density analysis on West Salem plot, likelihood of a tree being 
# in a site
TREE_DENSITY = 0.01071632 * SITE_SIZE * SITE_SIZE

# CDF of percentages from tree ratings in 2002 
# (original values {0.2356828, 0.2048458, 0.5594714})
BEGIN_RATING = [0.2356828, 0.4405286, 1]

# CDF of percentages from tree stages in 2002 
# (orig. values {0.1059603, 0.4282561, 0.2030905, 0.2626932})
BEGIN_STAGE = [0.1059603, 0.5342164, 0.7373069, 1]

# Probability of a virulent tree sporing event
PROB_OF_SPORE_VIRU = 1 - math.exp(-1.5)

# Probability of a hypovirulent tree sporing event
PROB_OF_SPORE_HYPO = 1 - math.exp(-.75)

# Previously used to calculate the number of infections. 
# Usage:   
# maxInfections = (int) math.round(math.exp(config.NUM_INF_CDF[0]*math.random()- config.NUM_INF_CDF[1]))
# Now is used to calculate the MAX number of infections.
NUM_INF_CDF = [5.6117, 3.6341]

# Percentage of infections from HV trees that result in HV infections 
# (otherwise virulent infection)
PER_HV_TO_HV = 0.65

# NEW Distance Coefficients for Infect (4/22/18).
# Each instance represents a probability for an infection on 8m intervals
# e.g. 0.3915 probability spread 8m, 0.5195 probaility 16m, ...
V_INFECT_RANGE_PROB_8M_INT = [
    0.3915, 0.5195, 0.6081, 0.6706, 0.7188, 0.7580, 
    0.7912, 0.8199, 0.8451, 0.8677, 0.8882, 0.9068,
    0.9239, 0.9398, 0.9545, 0.9683, 0.9813, 0.9935, 
    1.0000
]

# NEW Distance Coefficients for Infect (4/22/18).
# Each instance represents a probability for an infection on 8m intervals
HV_INFECT_RANGE_PROB_8M_INT = [
    0.5746, 0.6587, 0.7169, 0.7578, 0.7894, 0.8152, 0.8370, 0.8558, 0.8724, 
    0.8872, 0.9006, 0.9129, 0.9241, 0.9345, 0.9442, 0.9533, 0.9618, 0.9698, 
    0.9774, 0.9846, 0.9914, 0.9979, 1.0000
]

# Population dynamics of West Salem in 2002. Rows are virulent, hypovirulent 
# and healthy. Each entry corresponds to a stage (size).
POP_2002_CDF = [
    0.03311258, 0.09050773, 0.15011038, 0.23399558, 0.23399558, 0.27373068, 
    0.31567329, 0.43929360, 0.51214128, 0.84326711, 0.94481236, 1.00000000
]

# Used to calculate new ratings of trees in getNextYear(). Implementation is 
# not exactly clear as to what is happening.
NEW_RATING_CDF = [
    [0.69714286, 1],
    [0.20588235, 1],
    [0.52651515, 1],
    [0.09884467, 1]
]

# Used to calculate new stages of trees in getNextYear().  
# Implementation is not exactly clear as to what is happening.
NEW_STAGE_CDF = [
    [0.2, 0.962, 0.999, 0.999, 1],
    [0.006, 0.09, 0.99, 1, 1],
    [0.05, 0.05,0.3, 0.96,1], 
    [0.021, 0.021, 0.101, 0.111, 1], 
    [0.18, 0.996, 1, 1, 1], 
    [0, 0.09, 0.98, 1, 1], 
    [0.01, 0.01, 0.05, 0.96, 1], 
    [0.001, 0.001, 0.006, 0.056, 1], 
    [0.16, 0.994, 1, 1, 1],
    [0, 0.07, 0.99, 1, 1],
    [0, 0, 0, 0.95, 1],
    [0.013, 0.013, 0.013, 0.013, 1]
]

"""
-------------------------------------------------------
              NEURAL NETWORK SETTINGS
-------------------------------------------------------
""" 
# # of input nodes for neural network classifier 
# (rating, stage, virulent neighbors, hypo-virulent neighbors, healthy neighbors)
INPUT_LAYER_NODE_COUNT = 5

# # of hidden nodes for neural network classifier
HIDDEN_LAYER_NODE_COUNT = 10
# # of output nodes for neural network classifier (good, bad)
OUTPUT_LAYER_NODE_COUNT = 2
# Defines the square range (NEIGHBOR_RADIUSxNEIGHBOR_RADIUS) of SITESIZE tiles 
# to look at when determining the neighbors of a tree. The neighbors are used 
# for Q-Learning. A higher neighbor_radius means a larger state space.
NEIGHBOR_RADIUS = 4