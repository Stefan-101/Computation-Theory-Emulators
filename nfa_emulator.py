# The following emulator takes in an NFA (can be created with c_parser) and consumes letters/strings
# while modifying the state of the emulator.
# Letters are separted by single spaces.

from nfa_checker import check
import re

class Emulator:
    def __init__(self, nfa):
        if check(nfa):
            raise Exception("Invalid NFA")
        
        # initialize the emulator
        self.alphabet = nfa["sigma"]
        self.current_states = [nfa["start"][0]]
        self.final_states = nfa["final"]
        self.read_first_letter = False  # if the first letter has been read
        self.rules = {}
        for rule in nfa["delta"]:
            rule = re.split("[ ,]+", rule)
            if (rule[0], rule[1]) in self.rules:
                self.rules[(rule[0], rule[1])].append(rule[2])
            else:
                self.rules[(rule[0], rule[1])] = [rule[2]]

    
    def get_current_states(self):
        return self.current_states
    
    def epsilon_closure(self):
        # returns current_states + states that can be reached by epsilon transitions

        closure = set(self.current_states)
        stack = list(self.current_states)

        while len(stack) > 0:
            state = stack.pop()
            if (state, "epsilon") in self.rules:
                for state in self.rules[(state, "epsilon")]:
                    if state not in closure:
                        closure.add(state)
                        stack.append(state)

        return list(closure)
    
    def consume_letter(self, letter):
        if letter not in self.alphabet:
            raise Exception("Invalid letter")
        
        if self.read_first_letter == False:
            self.current_states = self.epsilon_closure()
            self.read_first_letter = True

        # calculate the next states
        new_states = {}
        for i in range(len(self.current_states)):
            if (self.current_states[i], letter) in self.rules:
                new_states[self.current_states[i]] = self.rules[(self.current_states[i], letter)]
            else:
                new_states[self.current_states[i]] = []
           
        for i in range(len(self.current_states) - 1, -1, -1):
            if self.current_states[i] in new_states:
                self.current_states[i:i + 1] = new_states[self.current_states[i]]

        # calculate epsilon closure
        self.current_states = self.epsilon_closure()

    def consume_string(self, str):
        str = str.split()
        for letter in str:    
            self.consume_letter(letter)

    def is_accepted(self):
        return any(state in self.final_states for state in self.current_states)


                




                

                

    
