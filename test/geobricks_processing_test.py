import unittest
from shutil import rmtree
import os
from geobricks_processing.core import processing_core

path = "../test_data/burundi_maize_area/"
source_path = [path + "/burundi_maize_area_3857.tif"]
output_path = path + "/gdalwarp"
if os.path.isdir(output_path): rmtree(output_path)

processing_gdalwarp = [
    {
        "source_path": source_path,
        "output_path": output_path,
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


class GeobricksProcessingTest(unittest.TestCase):

    def test_processing_gdalwarp_gdaladdo(self):
        outputfiles = processing_core.process_data(processing_gdalwarp)
        self.assertEqual(len(outputfiles), 1)