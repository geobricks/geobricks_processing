Geobricks Processing
====================

The Geobricks processing library provides an easy way to process sets of layers, providing band extraction and some of the GDAL basic funcionalities. 
i.e. example:

gdalwarp example

```json
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
}
```



