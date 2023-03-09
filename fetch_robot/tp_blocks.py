from .tp_parameters import BLUE, ORANGE, PINK, GREEN, thr_dist_observation
from math import sqrt


class Blocks:
    def __init__(self):
        self.all_avbl = {'blue': BLUE, 'orange': ORANGE, 'pink': PINK, 'green': GREEN}

    def color2id(self, color, markers_info, location):
        min_dist = 10**5
        pick_id = -1
        for i in self.all_avbl[color]:
            if i in markers_info:
                map_distance2 = (markers_info[i][1][0] - location[0])**2 + (markers_info[i][1][1] - location[1])**2 + (markers_info[i][1][2] - location[2])**2
                map_distance = sqrt(map_distance2)
                if markers_info[i][3] < min_dist and map_distance < thr_dist_observation:
                    pick_id = i
                    min_dist = markers_info[i][3]

        try:
            self.all_avbl[color].remove(pick_id)
        except ValueError:
            pass

        return pick_id

