Geobricks Processing
====================

The Geobricks processing library provides an easy way to process sets of layers, providing band extraction and some of the GDAL basic funcionalities. 

Installation
============
The plug-in is distributed through PyPi and can be installed by typing the following command in the console:
```
pip install geobricksmodis
```
Examples
========

GDALWARP example

```python

from geobricks_processing.core import processing_core

processing_gdalwarp = {
    #Mandatory: "Array containing the source paths i.e. a layer of *.tif for band extraction or merging"
    "source_path": ["data/burundi_maize_area_3857.tif"],
    # Mandatory: String containing the output path. If it doesn't exists it will be created
    "output_path": "data/gdalwarp/",
    # Optional: String containing the output file name. If it doesn't exists it will be created with a uuid function
    "output_file_name": "burundi_maize_area_4326.tif",
    # Optional: Default band extraction is 1
    "band": 1,
    # Mandatory: Array with a list of operation (i.e. gdalwarp, gdaladdo, gdal_translate, band_extraction)
    "process": [
        {
            "gdalwarp": {
    # Optional: containing the command options
                "opt": {
                    "-multi": "",
                    "-overwrite": "",
                    "-of": "GTiff",
                    "-s_srs": "EPSG:3857",
                    "-t_srs": "EPSG:4326"
                }
            }
        }
    ]
}

output_files = processing_core.process_data(processing_gdalwarp)
```

To do more than one operation can be created an array containing the different steps of the process. In this example will be applied first a GDALWARP and then a GDALADDO operation to the output file.

```python
from geobricks_processing.core import processing_core

processing_gdalwarp = [
    {
        "source_path": ["data/burundi_maize_area_3857.tif"],
        "output_path": "data/gdalwarp/",
        "output_file_name": "burundi_maize_area_4326.tif",
        "band": 1,
        "process": [
            {
                "gdalwarp": {
                    "opt": {
                        "-multi": "",
                        "-overwrite": "",
                        "-of": "GTiff",
                        "-s_srs": "EPSG:3857",
                        "-t_srs": "EPSG:4326"
                    }
                }
            }
        ]
    },
    {
        "band": 1,
        "process": [
            {
                "gdaladdo": {
                    "parameters": {
                        # "--config": "BIGTIFF_OVERVIEW IF_NEEDED"
                    },
                    "overviews_levels": "2 4 8 16"
                }
            }
        ]
    }
]

output_files = processing_core.process_data(processing_gdalwarp)
```


