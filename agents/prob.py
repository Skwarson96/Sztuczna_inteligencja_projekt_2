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
        self.visited_loc.append(loc)
        self.dirs = ['N', 'E', 'S', 'W']
        self.moves = []
        self.prev_state = loc
        self.percept = []
        self.prob_pits_list = []
        self.real_prev_action = None
        self.bump_counter = 0
        self.test_prev_action = 'N'
        # ---------------------------------------

        self.comp_value_and_policy()

    def comp_value_and_policy(self):
        gamma = 0.9
        eps_V = 1e-6

        iter = 0
        # compute self.V and self.pi
        # TODO PUT YOUR CODE HERE

        converged = False
        while not converged:
            prev_V = np.copy(self.V)
            for state in self.locations:
                best_V = -1000
                best_action = 'N'
                for action in self.dirs:
                    curr_V = 0
                    reward = 0
                    if action == 'N':
                        self.moves = [(0, 1), (1, 0), (-1, 0)]
                    if action == 'E':
                        self.moves = [(1, 0), (0, 1), (0, -1)]
                    if action == 'S':
                        self.moves = [(0, -1), (1, 0), (-1, 0)]
                    if action == 'W':
                        self.moves = [(-1, 0), (0, 1), (0, -1)]

                    next_states = []
                    for move in self.moves:
                        if (state[0] + move[0], state[1] + move[1]) in self.locations:
                            next_states.append((state[0] + move[0], state[1] + move[1]))
                        else:
                            next_states.append(state)

                    for idx, next_state in enumerate(next_states):
                        # prawdopodobienstwo
                        prob = 0
                        if idx == 0:
                            prob = 0.9 # prawdopodobienstwo wykonania zaplanowanej akcji
                        else:
                            prob = 0.05 # prawdopodobinstwo wykonania ruchu w bok ( nie zaplanoawna akcja)

                        # nagroda
                        R = 0
                        if (next_state not in self.visited_loc) and (next_state not in self.prob_pits_list):
                            R = 100 # nagroda za odkrycie nowego pola
                        else:
                            R = -10 # kara za wejście na odwiedzone juz pole

                        if next_state in self.prob_pits_list:
                            R = -100 # kara za wejscie na pole na ktorym prawdopodobnie jest dol

                        if next_state in self.pits_list:
                            R = -10000 # kara za wejscie na pole ktore jest na liscie dolow

                        next_state_index = self.loc_to_idx[next_state]
                        V_next_state = prev_V[next_state_index]

                        reward = gamma * R
                        curr_V += prob * (reward + gamma * V_next_state)

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

            iter += 1

        # wyswietlanie macierzy self.V razem z lokacjami
        # self.printing_matrix()
        # -----------------------

        print('Policy found after ', iter, ' iterations')


    def printing_matrix(self):
        first_row = []
        second_row = []
        third_row = []
        fourth_row = []
        for idx, (x, y) in enumerate(self.locations):

            if y == 6:
                first_row.append(((x, y), self.V[idx], self.pi[idx]))
            if y == 7:
                second_row.append(((x, y), self.V[idx], self.pi[idx]))
            if y == 8:
                third_row.append(((x, y), self.V[idx], self.pi[idx]))
            if y == 9:
                fourth_row.append(((x, y), self.V[idx], self.pi[idx]))

        fourth_row = sorted(fourth_row)
        third_row = sorted(third_row)
        second_row = sorted(second_row)
        first_row = sorted(first_row)

        print(fourth_row)
        print(third_row)
        print(second_row)
        print(first_row)

    def get_policy(self):
        pi_dict = {loc: self.pi[i] for i, loc in enumerate(self.locations)}
        return pi_dict

    def __call__(self, percept, loc):
        self.loc = loc

        # update the policy
        # TODO PUT YOUR CODE HERE
        self.percept = percept
        self.visited_loc.append(loc)
        self.prev_state = self.visited_loc[-2]
        # obliczenie poprzedniej akcji na podstawie zmiany wspolrzednych
        self.real_prev_action = 'S'
        # N (0, 1)
        # S (0, -1)
        # E (1, 0)
        # W (-1, 0)
        if (loc[0]- self.prev_state[0], loc[1] - self.prev_state[1]) == (0, 1):
            self.real_prev_action = 'N'
        if (loc[0]- self.prev_state[0], loc[1] - self.prev_state[1]) == (0, -1):
            self.real_prev_action = 'S'
        if (loc[0]- self.prev_state[0], loc[1] - self.prev_state[1]) == (1, 0):
            self.real_prev_action = 'E'
        if (loc[0]- self.prev_state[0], loc[1] - self.prev_state[1]) == (-1, 0):
            self.real_prev_action = 'W'
        # gdy agent nie ruszy sie z miejsca
        if (loc[0]- self.prev_state[0], loc[1] - self.prev_state[1]) == (0, 0):
            self.real_prev_action = self.prev_action

        # self.prev_action = self.real_prev_action


        # po wejsciu do lokacji z dolem, doanie lokacji do listy
        if 'pit' in percept and loc not in self.pits_list:
            self.pits_list.append(loc)

        # znajdywanie miejsc w któchych prawdopodobnie jest pit
        if ('breeze' in percept) and (loc not in self.breeze_list): # and (loc not in self.prob_pits_list):
            self.breeze_list.append(loc)
            moves = []

            if self.real_prev_action == 'N':
                moves = [(0, 1), (1, 0), (-1, 0)]
            if self.real_prev_action == 'E':
                moves = [(1, 0), (0, 1), (0, -1)]
            if self.real_prev_action == 'S':
                moves = [(0, -1), (1, 0), (-1, 0)]
            if self.real_prev_action == 'W':
                moves = [(-1, 0), (0, 1), (0, -1)]

            for move in moves:
                if (loc[0] + move[0], loc[1] + move[1]) in self.locations:
                    self.prob_pits_list.append((loc[0] + move[0], loc[1] + move[1]))

        # usuniecie lokalizacji jezeli zostala odwiedzona
        for state in self.visited_loc:
            if state in self.prob_pits_list:
                self.prob_pits_list.remove(state)

        # Jezeli do self.prob_pits_list zostanie dodana dwa razy ta sama lokalizacja to oznacza ze na 100% jest tam pit
        set_prob_pits = set()
        for prob_pit in self.prob_pits_list:
            if prob_pit in set_prob_pits:
                self.pits_list.append(prob_pit)
                self.prob_pits_list.remove(prob_pit)
                self.prob_pits_list.remove(prob_pit)
            else:
                set_prob_pits.add(prob_pit)

        # znalezienie akcji przeciwej do poprzedniej akcji
        oposite_action = 'S'
        if self.real_prev_action == 'N':
            oposite_action = 'S'
        if self.real_prev_action == 'E':
            oposite_action = 'W'
        if self.real_prev_action == 'S':
            oposite_action = 'N'
        if self.real_prev_action == 'W':
            oposite_action = 'E'

        if 'bump' in self.percept:
            self.bump_counter += 1
        else:
            self.bump_counter = 0
        # jezeli bedzie 5 razy bump to zostanie wymuszona przeciwna akcja
        if self.bump_counter == 5:
            action = oposite_action
            return action

        self.comp_value_and_policy()

       # -----------------------

        # choose action according to policy
        action = self.pi[self.loc_to_idx[self.loc]]
        self.prev_action = action

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
