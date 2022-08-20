from math import pi
BLUE = list(range(61, 79))
# ORANGE = list(range(43, 61))
ORANGE = [53, 45]
PINK = list(range(25, 43))
GREEN = list(range(79, 97))

PICK_TABLE_POS = {1: [1.21, -1.44, 0],
                  2: [1.21, -1.44, 0],
                  3: [-2.184, 0.46, 0],
                  4: [-2.184, 0.46, 0]}  # 1&2 computer table

PLACE_TABLE_POS = {1: [-2.4, -0.71, pi],
                   2: [],
                   3: [],
                   4: [],
                   5: []}

PLACE_IDS = {1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4},
             2: {1: 5, 2: 6, 3: 7, 4: 8, 5: 9},
             3: {1: 10, 2: 11, 3: 12, 4: 13, 5: 14},
             4: {1: 15, 2: 16, 3: 17, 4: 18, 5: 19}}
