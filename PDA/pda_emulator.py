# The following emulator takes in a PDA (can be created with c_parser) and consumes letters/strings
# while modifying the state of the emulator.
# Letters are separted by single spaces inside a string.

from PDA.pda_checker import check
import re

class Rule_output:
    # A PDA rule output is a state to which the PDA transitions, and a stack_letter that gets pushed onto the stack
    def __int__(self, state, stack_letter):
        self.state = state
        self.stack_letter = stack_letter

class Emulator:
    def __init__(self, pda):
        """
        Initialize the emulator with a PDA as outputed by c_parser
        """
        if check(pda):
            raise Exception("Invalid PDA")
        
        # initialize the emulator
        self.input_alphabet = pda["inputsigma"]
        self.stack_alphabet = pda["stacksigma"]
        self.current_state = pda["start"][0]
        self.final_states = pda["final"]
        self.stack = ['$']      # we use the $ symbol to represent the bottom of the stack

        self.rules = {}
        for rule in pda["delta"]:
            rule = re.split("[ ,]+", rule)

            rule_output = Rule_output()
            rule_output.state = rule[3]
            rule_output.stack_letter = rule[4]

            self.rules[(rule[0], rule[1], rule[2])] = rule_output

    def get_current_state(self):
        """
        Returns the current state of the PDA and its stack
        """
        return {"state": self.current_state, "stack": self.stack}
        
    def consume_letter(self, input_letter):
        """
        Consumes an input letter and modifies the state of the PDA
        """
        if input_letter not in self.input_alphabet:
            raise Exception("Invalid letter")
        
        try:
            stack_top = self.stack.pop()
        except IndexError:
            stack_top = None
        
        rule_input = (self.current_state, input_letter, stack_top)
        if rule_input in self.rules:
            rule_output: Rule_output = self.rules[rule_input]
            self.current_state = rule_output.state
            if rule_output.stack_letter != "epsilon":
                self.stack.append(rule_output.stack_letter)
            return
        
        # if no rule is found, we need to put the stack top back and 
        # look for rules that don't pop from the stack (epsilon stack letter)
        self.stack.append(stack_top)
        for rule in self.rules:
            if rule[0] == self.current_state and rule[1] == input_letter and rule[2] == "epsilon":
                rule_output: Rule_output = self.rules[rule]
                self.current_state = rule_output.state
                if rule_output.stack_letter != "epsilon":
                    print(rule_output.stack_letter)
                    self.stack.append(rule_output.stack_letter)
                return

        # if no rule is found, the PDA goes to a "dead state" 
        self.current_state = "NO_STATE"

    def consume_string(self, str):
        """
        Consumes a string of letters and modifies the state of the PDA
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
    