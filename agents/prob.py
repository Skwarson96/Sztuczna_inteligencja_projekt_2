# prob.py
# This is

import random
import numpy as np

from gridutil import *


class LocAgent:
    def __init__(self, size, walls, eps_move, npits, loc):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {iloc: idx for idx, iloc in enumerate(self.locations)}
        self.eps_move = eps_move
        self.npits = npits
        self.loc = loc

        # previous action
        self.prev_action = None

        self.t = 0

        self.V = np.zeros([len(self.locations)], dtype=np.float)
        self.pi = ['E' for _ in self.locations]

        # TODO PUT YOUR ADDITIONAL VARIABLES HERE

        self.pits_list = []
        self.breeze_list = []
        self.visited_loc = []
        self.dirs = ['N', 'E', 'S', 'W']
        self.next_state = []
        self.t = 0
        self.gamma = 0.9
        # ---------------------------------------

        self.comp_value_and_policy()

    def comp_value_and_policy(self):
        reward_gold = 10
        reward_pits = -100
        gamma = 0.9
        eps_V = 1e-6

        iter = 0
        pass
        # compute self.V and self.pi
        # TODO PUT YOUR CODE HERE


        # dirs = ['N', 'E', 'S', 'W']
        #
        # for i, pi in enumerate(self.pi):
        #     self.pi[i] = random.choice(dirs)



        converged = False
        while not converged:
            prev_V = self.V.copy()
            for state in self.locations:
                best_V = -1000
                best_action = 'N'
                for action in self.dirs:
                    curr_V = 0
                    if action == 'N':
                        self.next_state = [(0, 1), (1, 0), (-1, 0)]
                    if action == 'E':
                        self.next_state = [(1, 0), (0, 1), (0, -1)]
                    if action == 'S':
                        self.next_state = [(0, -1), (1, 0), (-1, 0)]
                    if action == 'W':
                        self.next_state = [(-1, 0), (0, 1), (0, -1)]
                    print('action:', action, 'next states:', self.next_state)

                    for idx, move in enumerate(self.next_state):
                        prob = 0
                        if idx == 0:
                            prob = 0.9
                        else:
                            prob = 0.05
                        # TODO
                        # jezeli nastepny stan to bryza to trzeba dac kare
                        # jezeli nastepny stan to dol to rzeba dac kare

                        # next_loc = loc + move
                        # if next_loc in self.pits_list:
                        #     R = -100
                        # if next_loc in self.breeze_list:
                        #     R = -100

                        R = 0
                        V_move = prev_V

                        # curr_V += prob * (R * gamma ** iter * )
                    if curr_V > best_V:
                        best_V = curr_V
                        best_action = action

            # self.V[] = best_V
            # self.pi[] = best_action

            for idx, st in enumerate(self.V):
                if abs(prev_V[idx] - st) < eps_V:
                    converged = True
                else:
                    converged = False
                    break
            iter += 1


        # print('self.V')
        # print(np.shape(self.V))
        # print(self.V)
        # print('self.pi')
        # print(np.shape(self.pi))
        # print(self.pi)

        # -----------------------

        print('Policy found after ', iter, ' iterations')



    def get_policy(self):
       pi_dict = {loc: self.pi[i] for i, loc in enumerate(self.locations)}
       # print(pi_dict)
       return pi_dict

    def __call__(self, percept, loc):
       self.loc = loc

       # update the policy
       # TODO PUT YOUR CODE HERE

       if 'pit' in percept and loc not in self.pits_list:
           self.pits_list.append(loc)
           print('self.pits_list', self.pits_list)
       if 'breeze' in percept and loc not in self.breeze_list:
           # print("TEST breeze")
           self.breeze_list.append(loc)
           print('self.breeze_list', self.breeze_list)

       self.comp_value_and_policy()



       # -----------------------

       # choose action according to policy
       action = self.pi[self.loc_to_idx[self.loc]]

       return action

    def forward(self, cur_loc, cur_dir):
       if cur_dir == 'N':
           ret_loc = (cur_loc[0], cur_loc[1] + 1)
       elif cur_dir == 'E':
           ret_loc = (cur_loc[0] + 1, cur_loc[1])
       elif cur_dir == 'W':
           ret_loc = (cur_loc[0] - 1, cur_loc[1])
       elif cur_dir == 'S':
           ret_loc = (cur_loc[0], cur_loc[1] - 1)
       ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
       return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
       if cur_dir == 'N':
           ret_loc = (cur_loc[0], cur_loc[1] - 1)
       elif cur_dir == 'E':
           ret_loc = (cur_loc[0] - 1, cur_loc[1])
       elif cur_dir == 'W':
           ret_loc = (cur_loc[0] + 1, cur_loc[1])
       elif cur_dir == 'S':
           ret_loc = (cur_loc[0], cur_loc[1] + 1)
       ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
       return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
       dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
       dirs = ['N', 'E', 'S', 'W']
       idx = (dir_to_idx[cur_dir] + 1) % 4
       return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
       dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
       dirs = ['N', 'E', 'S', 'W']
       idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
       return cur_loc, dirs[idx]
