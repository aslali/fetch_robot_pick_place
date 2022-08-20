from tp_parameters import BLUE, ORANGE, PINK, GREEN


class Blocks:
    def __init__(self):
        # self.blue_avbl = BLUE[:]
        # self.orange_avbl = ORANGE[:]
        # self.pink_avbl = PINK[:]
        # self.green_avbl = GREEN[:]
        self.all_avbl = {'b': BLUE, 'o': ORANGE, 'p': PINK, 'g': GREEN}

    def color2id(self, color, markers_info):
        # all_avbl = {'b': self.blue_avbl, 'o': self.orange_avbl, 'p': self.pink_avbl, 'g': self.green_avbl}
        min_dist = 10**5
        pick_id = -1
        for i in self.all_avbl[color]:
            if i in markers_info:
                if markers_info[i][3] < min_dist:
                    pick_id = i
                    min_dist = markers_info[i][3]

        try:
            self.all_avbl[color].remove(pick_id)
            print(self.all_avbl)
        except ValueError:
            pass

        return pick_id

