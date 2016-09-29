# weather at home

weatherathome functionality

## Usage

Unzip folders

```python
import weatherathome as wah
# unzip month_index 7 (= June) monthly regional file
wah.unzip('/path/w_at_h/hadam3p_eu_2014', '*_7.zip', '*ga.pe*')
```

Obtain list of available folders
```python
import weatherathome as wah
# read all simulations months
w = wah.wah('/path/w_at_h/hadam3p_eu/hadam3p_eu_*[!zip]')

# subset
ws = w.select(year=2014, month=slice(6, 8))

umid_unique = ws.UMID_number_unique

for ui in umid_unique:
    ws.load_regional_monthly('precipitation_flux', UMID_number=ui)
```


