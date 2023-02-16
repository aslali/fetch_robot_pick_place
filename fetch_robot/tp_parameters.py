from math import pi
BLUE = list(range(61, 79))
ORANGE = list(range(43, 61))
# ORANGE = [53, 45]
PINK = list(range(25, 43))
GREEN = list(range(79, 97))
BLOCK_LOCATIONS = {'blue': 1, 'orange': 1, 'green': 2, 'pink':2}
PICK_TABLE_POS = {1: [0.858, -1.164, 0.0],
                  2: [-2.354, 0.680, 0.0]}

PLACE_TABLE_POS = {1: [-2.636, -0.257, pi],
                   2: [],
                   3: [],
                   4: [],
                   5: []}

PLACE_IDS = {1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4},
             2: {1: 5, 2: 6, 3: 7, 4: 8, 5: 9},
             3: {1: 10, 2: 11, 3: 12, 4: 13, 5: 14},
             4: {1: 15, 2: 16, 3: 17, 4: 18, 5: 19}}

thr_dist_observation = 1.8
