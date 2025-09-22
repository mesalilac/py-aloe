"""Usage:
```python

from py_cfg import Cfg

cfg = Cfg.from_file("...")

default_username = cfg.get("default_username")

print(default_username)

cfg.set("default_username", "admin")

cfg.save()
```
"""

from .cfg import Cfg
