# The following emulator takes in a DFA (can be created with c_parser) and consumes letters/strings
# while modifying the state of the emulator.
# Letters are separted by single spaces inside a string.

from DFA.dfa_checker import check
import re

class Emulator:
    def __init__(self, dfa):
        """
        Initialize the emulator with a DFA as outputed by c_parser
        """
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
        """
        Returns the current state of the DFA
        """
        return self.current_state
        
    def consume_letter(self, letter):
        """
        Consumes a letter and modifies the state of the DFA
        If no rule is found, the state is set to "NO_STATE"
        """
        if letter not in self.alphabet:
            raise Exception("Invalid letter")
        
        if (self.current_state, letter) in self.rules:
            self.current_state = self.rules[(self.current_state, letter)]
        else:
            self.current_state = "NO_STATE"     # if no rule is found, the DFA goes to a "dead state"

    def consume_string(self, str):
        """
        Consumes a string of letters and modifies the state of the DFA
        Letters are separated by single spaces
        """
        str = str.split()
        for letter in str:  
            self.consume_letter(letter)
        
    def is_accepted(self):
        """
        Returns True if the current state is a final state
        """
        return self.current_state in self.final_states
    