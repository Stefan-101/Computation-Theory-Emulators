import CFG.cfg_checker as cfg_checker
import re
import random

class Emulator:
    def __init__(self, cfg):
        """
        Initializes the emulator with the given CFG
        """
        if cfg_checker.check(cfg):
            raise Exception("Invalid CFG")
        
        # initialize the emulator
        self.current_string = ' ' + re.split("\s*->\s*", cfg["rules"][0])[0] + ' '
        self.terminals = cfg["sigma"]
        self.vars = cfg["vars"]

        self.rules = {}
        for rule in cfg["rules"]:
            rule = re.split("\s*->\s*", rule)
            if rule[0] in self.rules:
                self.rules[rule[0]].extend(re.split("\s*\|\s*", rule[1]))
            else:
                self.rules[rule[0]] = re.split("\s*\|\s*", rule[1])

    def get_current_string(self):
        """
        Returns the string generated to the current point.
        """
        return self.current_string
    
    # step function attempts to replace a variable and returns True if it was successful
    def step(self, steps = 1):
        """
        Replaces a variable in the current string with its rule (or a random rule if it has multiple rules).
        """
        for _ in range(steps):
            # identify a variable present in the string
            var = None
            for v in self.vars:
                if v in self.current_string.split():
                    var = v
                    break

            # replace var with its rule (random if it has multiple rules)
            if var is not None:
                rule = self.rules[var]
                rule = random.choice(rule)   # choose a random rule

                if rule != "epsilon":
                    self.current_string = self.current_string.replace(' ' + var + ' ', ' ' + rule + ' ', 1)
                else:
                    self.current_string = self.current_string.replace(' ' + var + ' ', ' ', 1)
            else:
                # no more variables in the string, remove leftover spaces and return
                self.current_string = self.current_string.strip()
                return False
        return True
        
