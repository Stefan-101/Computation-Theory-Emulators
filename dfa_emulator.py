# The following emulator takes in a DFA (can be created with c_parser) and consumes letters/strings
# while modifying the state of the emulator.
# Letters are separted by single spaces.

from dfa_checker import check
import re

class Emulator:
    def __init__(self, dfa):
        if check(dfa):
            raise Exception("Invalid DFA")
        
        # initialize the emulator
        self.alphabet = dfa["sigma"]
        self.current_state = dfa["start"][0]
        self.final_states = dfa["final"]
        self.rules = {}
        for rule in dfa["delta"]:
            rule = re.split("[ ,]+", rule)
            self.rules[(rule[0], rule[1])] = rule[2]

    def get_current_state(self):
        return self.current_state
        
    def consume_letter(self, letter):
        if letter not in self.alphabet:
            raise Exception("Invalid letter")
        
        if (self.current_state, letter) in self.rules:
            self.current_state = self.rules[(self.current_state, letter)]
        else:
            self.current_state = "NO_STATE"

    def consume_string(self, str):
        str = str.split()
        for letter in str:
            if letter not in self.alphabet:
                raise Exception("Invalid letter")
            
            if (self.current_state, letter) in self.rules:
                self.current_state = self.rules[(self.current_state, letter)]
            else:
                self.current_state = "NO_STATE"
        
    def is_accepted(self):
        return self.current_state in self.final_states
    