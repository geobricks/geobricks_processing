Examples
========
Get MODIS products list
-----------------------
```python
from geobricks_modis.core import modis_core as c


products = c.list_products()
```
Get available years
-------------------
```python
from geobricks_modis.core import modis_core as c


years = c.list_years('MOD13A2')
```
Get available days
------------------
```python
from geobricks_modis.core import modis_core as c


days = c.list_days('MOD13A2', '2010')
```
Get available layers
--------------------
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers('MOD13A2', '2010', '001')
```
Get a subset of layers
----------------------
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_subset('MOD13A2', '2010', '001', 5, 7, 3, 9)
```
Get layers by country GAUL code
-------------------------------
This method retrieves the list of MODIS tiles for the given product, year and day, filtered by the country GAUL code. The example below gets the layers of Afghanistan (1) and Angola (8).
```python
from geobricks_modis.core import modis_core as c


layers = c.list_layers_countries_subset('MOD13A2', '2010', '001', '8,1')
```
Get layers by country ISO2 code
-------------------------------
TBD.
