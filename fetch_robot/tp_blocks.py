from .tp_parameters import BLUE, ORANGE, PINK, GREEN


class Blocks:
    def __init__(self):
        self.all_avbl = {'b': BLUE, 'o': ORANGE, 'p': PINK, 'g': GREEN}

    def color2id(self, color, markers_info):
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

