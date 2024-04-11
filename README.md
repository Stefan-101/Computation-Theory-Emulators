# Example usage
Example usage with a DFA:  

```
from dfa_emulator import Emulator
import c_parser

em = Emulator(c_parser.load_file("DFA_Examples/dfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current state: " + em.get_current_state())
print("Is accepted: " + str(em.is_accepted()))
```

Example usage with a NFA:

```
from nfa_emulator import Emulator
import c_parser

em = Emulator(c_parser.load_file("NFA_Examples/nfa1.config"))
em.consume_letter("0")
em.consume_string("0 1 1")
print("Current states: " + str(em.get_current_states()))
print("Is accepted: " + str(em.is_accepted()))
```