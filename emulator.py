# The following emulator takes in a DFA (can be created with c_parser) and consumes letters/strings
# while modifying the state of the emulator.
# Letters are separted by single spaces.

from dfa_checker import check
import re

class Emulator:
    def __init__(self, dfa):
        if check(dfa):
            raise Exception("Invalid DFA")
        self.dfa = dfa
        self.current_state = dfa["start"][0]

    def consume_string(self, str):
        str = str.split()
        for letter in str:
            for rule in self.dfa["delta"]:
                rule = re.split("[ ,]+", rule)
                if rule[0] == self.current_state and rule[1].lower() == letter.lower():
                    self.current_state = rule[2]
                    break
        
    def consume_letter(self, str):
        for rule in self.dfa["delta"]:
            rule = re.split("[ ,]+", rule)
            if rule[0] == self.current_state and rule[1].lower() == str.lower():
                self.current_state = rule[2]
                break
        
    def is_accepted(self):
        return self.current_state in self.dfa["final"]
    