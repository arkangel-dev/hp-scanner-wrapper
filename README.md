# hp-scanner-wrapper
 Python wrapper for HP printers with scanner beds. Tested with HP 3-In-1 DeskJet 2630.

```python
from hpwrapper import Wrapper

scanner = Wrapper('http://192.168.100.80')
scanner.ScanDocument("ScanResult.png")
```

