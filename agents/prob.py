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
        self.moves = []
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

        converged = False
        while not converged:
            prev_V = np.copy(self.V)
            for state in self.locations:
                best_V = -1000
                best_action = 'N'
                # print('state:', state)
                for action in self.dirs:
                    curr_V = 0
                    if action == 'N':
                        self.moves = [(0, 1), (1, 0), (-1, 0)]
                    if action == 'E':
                        self.moves = [(1, 0), (0, 1), (0, -1)]
                    if action == 'S':
                        self.moves = [(0, -1), (1, 0), (-1, 0)]
                    if action == 'W':
                        self.moves = [(-1, 0), (0, 1), (0, -1)]
                    # print('action:', action, 'possible moves', self.moves)

                    next_states = []
                    for move in self.moves:
                        # print(state[0] + move[0], state[1] + move[1])
                        if (state[0] + move[0], state[1] + move[1]) in self.locations:
                            next_states.append((state[0] + move[0], state[1] + move[1]))
                        else:
                            next_states.append(state)
                    # print('next possible states: ', next_states)

                    for idx, next_state in enumerate(next_states):
                        # prawdopodobienstwo
                        prob = 0
                        if idx == 0:
                            prob = 0.9
                        else:
                            prob = 0.05

                        # nagroda
                        R = 0
                        # print('visited_loc', self.visited_loc)
                        if next_state in self.visited_loc and state in self.visited_loc:
                            R = -10.0
                        else:
                            R = 10.0
                        if next_state in self.breeze_list:
                            R = -100.0
                        if next_state in self.pits_list:
                            R = -10000.0

                        # print('next state idx', self.loc_to_idx[next_state])
                        next_state_index = self.loc_to_idx[next_state]
                        V_next_state = prev_V[next_state_index]

                        curr_V += prob * (R + gamma ** iter * V_next_state)

                        # print('prob:', prob, ', R:', R, ', gamma ** iter:', gamma ** iter, ' ,V_next_state:', V_next_state, 'curr_v:', curr_V)
                    if curr_V > best_V:
                        best_V = curr_V
                        best_action = action

                state_index = self.loc_to_idx[state]
                self.V[state_index] = best_V
                self.pi[state_index] = best_action

            for idx, st in enumerate(self.V):
                # print(idx, prev_V[idx],  st)
                if abs(prev_V[idx] - st) > eps_V:
                    converged = False
                    break
                else:
                    converged = True
            # for i in range(0, len(self.V)):
            #     if abs(prev_V[i] - self.V[i]) > eps_V:
            #         converged = False
            #         break
            #     converged = True

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

        if loc not in self.visited_loc:
            self.visited_loc.append(loc)

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
