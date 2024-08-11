import time

import numpy as np


class Stats:


    def __init__(self):
        self.start_time = time.perf_counter_ns()
        self.u = 0
        self.s = 0.18
        self.s_stop = 0.09
        self.d = 0.03
        self.v_max = 1
        self.a = 0.5
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 0, 1, 2, 3
        self.directionVectors_inverse = {
            (0, 1): self.NORTH,
            (1, 0): self.EAST,
            (0, -1): self.SOUTH,
            (-1, 0): self.WEST
        }

    def get_runtime(self):
        end_time = time.perf_counter_ns()
        return end_time - self.start_time

    def get_acceleration_time(self, s):
        final_velocity = np.sqrt(self.u ** 2 + 2 * self.a * s)
        # print(final_velocity)
        ceof = [0.5 * self.a, self.u, -s]
        roots = np.roots(ceof)
        t = roots[roots > 0][0]
        if final_velocity > self.v_max:
            print('gi')
            s_acc = (self.v_max ** 2 - self.u ** 2) / (2 * self.a)
            ceof = [0.5 * self.a, self.u, -s_acc]
            roots = np.roots(ceof)
            t_acc = roots[roots > 0][0]

            s_zero_acc = s - s_acc
            print(s, s_acc)
            t_zero_acc = s_zero_acc/self.v_max
            print(s_zero_acc, self.v_max, t_zero_acc)
            t = t_acc + t_zero_acc
        return t

    def get_turn_time(self, action, old_orientation):
        if action == (old_orientation + 2) % 4:
            return 0
        return np.sqrt((self.d * (np.pi/2)) / (2*self.a))

    def get_time_from_path(self, path):
        counter = 0
        previous_orientation = self.NORTH
        previous_position = path[0]
        tot_time = 0

        for position in path[1:]:
            dx, dy = position[0] - previous_position[0], position[1] - previous_position[1]
            orientation = self.directionVectors_inverse[(dx, dy)]
            if orientation == previous_orientation:
                counter += 1
                previous_position = position
                previous_orientation = orientation
                continue
            dist = (counter/2 * self.s) + self.s_stop
            t_acc_dec = self.get_acceleration_time(dist) * 2
            t_turn = self.get_turn_time(orientation, previous_orientation)
            t_acc = self.get_acceleration_time(self.s_stop)
            tot_time += t_acc_dec + t_turn + t_acc
            # print(position, t_acc_dec, t_turn, t_acc, tot_time)
            self.u = 0
            counter = 0
            previous_position = position
            previous_orientation = orientation

        return tot_time



