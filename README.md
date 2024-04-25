# Example usage
Example usage with a DFA:  

```
from DFA.dfa_emulator import Emulator
import utils.c_parser as c_parser

em = Emulator(c_parser.load_file("DFA_Examples/dfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current state: " + em.get_current_state())
print("Is accepted: " + str(em.is_accepted()))
```

Example usage with a NFA:

```
from NFA.nfa_emulator import Emulator
import utils.c_parser as c_parser

em = Emulator(c_parser.load_file("NFA_Examples/nfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current states: " + str(em.get_current_states()))
print("Is accepted: " + str(em.is_accepted()))
```

Example usage with a CFG:       

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