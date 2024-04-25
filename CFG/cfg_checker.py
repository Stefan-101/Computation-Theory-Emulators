import utils.c_parser as c_parser
import re

# The following check function returns different codes with the following meanings:
# 0 - No errors found
# 1 - Not all sections are present
# 2 - Sigma does not have any letter
# 3 - At least one of the vars does not start with an uppercase letter
# 4 - At least one of the rules contains a var which is not in the vars list
# 5 - At least one of the rules contains a component which is not in the vars or sigma list
#
# Set verbosity to 1 to print debug messages

def check(c, verbosity = 0):
    # check if all sections exist
    sections = ['vars', 'sigma', 'rules']
    for section in sections:
        if section not in c_parser.get_section_list(c):
            if verbosity:
                print(f"DEBUG: Section {section} is not defined")
            return 1

    # check if sigma has letters (terminals)
    if len(c_parser.get_section_content(c,"sigma")) == 0:
        if verbosity:
            print(f"DEBUG: Sigma has no letters")
        return 2

    # check Variables
    for var in c_parser.get_section_content(c,"vars"):
        # check if variable starts with uppercase letter
        if not var[0].isupper():
            if verbosity:
                print("The following var does not start with an uppercase letter:\n" + var)
            return 3
    
    # check rules
    for rule in c_parser.get_section_content(c,"rules"):
        rule = re.split("\s*->\s*", rule)

        # check if input var is in vars
        if rule[0] not in c_parser.get_section_content(c,"vars"):
            if verbosity:
                print("The following rule contains a var which is not in the vars list:\n" + rule)
            return 4
        
        # check if rule output is formed of correct variables and terminals
        output = rule[1].split()
        for component in output:
            if component not in c_parser.get_section_content(c,"vars") and component not in c_parser.get_section_content(c,"sigma"):
                if verbosity:
                    print("The following rule contains a component which is not in the vars or sigma list:\n" + ' -> '.join(rule))
                return 5

    return 0
