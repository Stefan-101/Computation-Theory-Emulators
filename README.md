# Parser and Emulators for CFG, DFA, NFA and PDA
### Parser (c_parser.py):
The parser is able to read a configuration file and return a dictionary that can be used by the emulators.      
It accepts blank lines and comments marked by #.        
It will raise an exception if the reserved keyword `NO_STATE` is found in the configuration file. See more about this below.          
Configuration files need to follow the section naming conventions presented in the example files corresponding to each emulator.        
__Special keyword:__ `epsilon` - represents the empty string (can be used for the NFA, PDA and CFG emulators)       
### Deterministic Finite Automata Emulator (DFA):       
See DFA/examples/dfa1.config for a DFA input example.       
The DFA has a `NO_STATE` state symbolizing being in a "dead state" (i.e. it won't be able to reach any other state).      

__Example usage:__      
```
from DFA.dfa_emulator import Emulator
import utils.c_parser as c_parser

em = Emulator(c_parser.load_file("DFA_Examples/dfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current state: " + em.get_current_state())
print("Is accepted: " + str(em.is_accepted()))
```

### Nondeterministic Finite Automate Emulator (NFA):        
See NFA/exmaples/nfa1.config for a NFA input example.       
Considering the nondeterministic nature, if multiple tranzitions are possible for the same input and current state, the emulator will "branch", keeping track of multiple active states and treating them independently for the letters that follow.
This emulator doesn't have a NO_STATE, instead it ends up not having any activate state on a given branch.      

__Example usage:__

```
from NFA.nfa_emulator import Emulator
import utils.c_parser as c_parser

em = Emulator(c_parser.load_file("NFA_Examples/nfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current states: " + str(em.get_current_states()))
print("Is accepted: " + str(em.is_accepted()))
```

### Context-Free Grammar Emulator (CFG):        
See CFG/examples/cfg1.config for a CFG input example.

__Example usage:__    

```
import utils.c_parser as c_parser
from CFG.cfg_emulator import Emulator

path = "CFG/examples/cfg2.config"
em = Emulator(c_parser.load_file(path))
i = 0
while i < 100:
    while em.step():
        pass

    print(f"{i + 1})", em.get_current_string())
    em = Emulator(c_parser.load_file(path))
    i += 1
```

### Pushdown Automata Emulator (PDA):
See PDA/examples/pda1.config for a PDA input example.       

__Example usage:__    

```
from PDA.pda_emulator import Emulator
import utils.c_parser as c_parser


em = Emulator(c_parser.load_file("PDA/examples/pda1.config"))
em.consume_string("0 0 0 1 1 1 @")
print("Current state: ", em.get_current_state())
print("Is accepted: " + str(em.is_accepted()))
```