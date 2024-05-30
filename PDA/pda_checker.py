import utils.c_parser as c_parser
import re

# The following check function returns different codes with the following meanings:
# 0 - No errors found
# 1 - Not all sections are present
# 2 - Alphabet does not have any letter
# 3 - Start state is not in state list
# 4 - At least one of the final state is not in state list
# 5 - At least one of the rules from the delta function is not a 5-tuple
# 6 - At least one of the rules from the delta function contains states which are not in the state list
# 7 - At least one of the rules from the delta function contains an input letter not present in the input alphabet
# 8 - At least one of the rules from the delta function contains a stack letter not present in the stack alphabet
#
# Set verbosity to 1 to print debug messages

def check(c, verbosity = 0):
    # check if all sections exist
    sections = ['inputsigma', 'stacksigma', 'states', 'start', 'final', 'delta']
    for section in sections:
        if section not in c_parser.get_section_list(c):
            if verbosity:
                print(f"DEBUG: Section {section} is not defined")
            return 1

    # check if both alphabets have letters
    if len(c_parser.get_section_content(c,"inputsigma")) == 0 or len(c_parser.get_section_content(c,"stacksigma")) == 0:
        if verbosity:
            print(f"DEBUG: Alphabet has no letters")
        return 2
    
    # check if start state is in state list
    for state in c_parser.get_section_content(c,"start"):
        if state not in c_parser.get_section_content(c,"states"):
            if verbosity:
                print("Start section is missing from section list")
            return 3
    # check if final states are in state list
    for state in c_parser.get_section_content(c,"final"):
        if state not in c_parser.get_section_content(c,"states"):
            if verbosity:
                print ("Final section " + section + " is missing from section list")
            return 4

    # check if delta is a valid function
    for rule in c_parser.get_section_content(c,"delta"):
        rule = re.split("[ ,]+", rule)

        # check if it is a 5-tuple
        if len(rule) != 5:
            if verbosity:
                print("The following rule is not a 5-tuple:\n" + rule)
            return 5

        # check if states from the rule are in the states list
        states_list = c_parser.get_section_content(c,"states")
        if rule[0] not in states_list or rule[3] not in states_list:
            if verbosity:
                print("The following rule contains states which are not in the states list:\n", rule)
            return 6
        
        input_sigma = c_parser.get_section_content(c,"inputsigma")
        if rule[1] not in input_sigma:
            if verbosity:
                print("The following rule takes an input letter which is not in the input alphabet:\n", rule) 
            return 7
        
        stack_sigma = c_parser.get_section_content(c,"stacksigma")
        if rule[2] not in stack_sigma and rule[2] != "$" and rule[2] != "epsilon":
            if verbosity:
                print("The following rule takes a stack letter which is not in the stack alphabet:\n", rule) 
            return 8
    return 0
