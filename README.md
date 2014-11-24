Geobricks Processing
====================

The Geobricks processing library provides an easy way to process sets of layers, providing band extraction and some of the GDAL basic funcionalities. 
i.e. example:

gdalwarp example

```python
{
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
```



