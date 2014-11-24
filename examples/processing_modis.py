from shutil import rmtree
import os
from geobricks_processing.core import processing_core

path = "../test_data/MODIS/MOD13A2"
source_path = [path + "/*.hdf"]
output_path = path + "/output"
if os.path.isdir(output_path):
    rmtree(output_path)

process_obj = [
    # extract of the band
    {
        "band": 1,
        "source_path": source_path,
        "output_path": output_path + "/extract_bands",
        "process": [
            {
                "extract_bands": ""
            }
        ]
    },
    # Merging of processed bands
    {
        "output_path": output_path + "/merged_bands",
        "output_file_name": "MOD13A2_merged.hdf",
        "process": [
            {
                "gdal_merge": {
                    "opt": {
                        "-n": "-3000",
                        "-a_nodata": "-3000"
                    }
                }
            }
        ]
    },
    {
        "output_path": output_path + "/gdalwarp",
        "output_file_name": "MOD13A2_3857.tif",
        "process": [
            {
                # 4326
                #"get_pixel_size": "{{PIXEL_SIZE}}/111195.496749"
                # 3857
                "get_pixel_size": "{{PIXEL_SIZE}}/2.00000000012"
            },
            {
                "gdalwarp": {
                    "opt": {
                        "-multi": "",
                        "-overwrite": "",
                        "-of": "GTiff",
                        "-s_srs": "'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
                        #"-t_srs": "EPSG:4326",
                        "-t_srs": "EPSG:3857",
                        "-tr": "{{PIXEL_SIZE}} -{{PIXEL_SIZE}}",
                        "-srcnodata": -3000,
                        "-dstnodata": -3000
                    }
                }
            }
        ]
    },
    {
        "output_path": output_path + "/gdal_translate",
        "output_file_name": "MOD13A2_3857.tif",
        "process": [
            {
                "gdal_translate": {
                    "opt": {
                        "-co": "'TILED=YES'",
                        "-co": "'COMPRESS=DEFLATE'",
                        "-a_nodata": -3000
                    }
                }
            }
        ]
    },
    {
        "process": [
            {
                "gdaladdo": {
                    "parameters": {
                        # "-r": "average"
                    },
                    "overviews_levels": "2 4 8 16"
                }
            }
        ]
    }
]

outputfiles = processing_core.process_data(process_obj)