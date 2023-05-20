from .tp_parameters import BLUE, ORANGE, PINK, GREEN, thr_dist_observation
from math import sqrt


class Blocks:
    def __init__(self):
        self.all_avbl = {'blue': BLUE, 'orange': ORANGE, 'pink': PINK, 'green': GREEN}
        self.color = None

    def color2id(self, color, markers_info, table_location, robot_location):
        print(markers_info)
        min_dist = 10**5
        pick_id = -1
        self.color = color
        for i in self.all_avbl[color]:
            if i in markers_info:
                map_distance2 = (markers_info[i][1][0] - table_location[0]) ** 2 + (markers_info[i][1][1] - table_location[1]) ** 2 + (markers_info[i][1][2] - table_location[2]) ** 2
                map_distance = sqrt(map_distance2)
                dist = (markers_info[i][1][0] - robot_location[0]) ** 2 + (markers_info[i][1][1] - robot_location[1]) ** 2 + (markers_info[i][1][2] - robot_location[2]) ** 2
                if dist < min_dist and map_distance < thr_dist_observation:
                    pick_id = i
                    min_dist = dist

        return pick_id

    def remove_id(self, pick_id):
        try:
            self.all_avbl[self.color].remove(pick_id)
        except ValueError:
            pass
