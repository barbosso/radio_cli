# radio_cli

simple cli radio on python

## bugs

File "/.env/lib/python3.10/site-packages/prompt_toolkit/styles/from_dict.py", line 9, in <module>
from collections import Mapping
ImportError: cannot import name 'Mapping' from 'collections'

### For fix need change file ".env/lib/python3.10/site-packages/prompt_toolkit/styles/from_dict.py"

```from collections import Mapping```

on

```
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
```
