from osgeo import gdal
import os
import subprocess
import json
import logging
import uuid
from geobricks_common.core.log import logger

log = logger(__file__)

# methods not related to a GDAL function
key_function = [
    "extract_bands",  # used to extract the bands
    "get_pixel_size"  # used to get the pixel size
]


def process_data(objs, loglevel=logging.INFO):
    """
    Process a json array with GDAL raster operations.
    @return: An array with the processed files.
    """
    result = []
    for obj in objs:
        obj["source_path"] = obj["source_path"] if "source_path" in obj else result
        result = process_obj(obj, loglevel)
    return result


def process_obj(obj, loglevel=logging.INFO):
    """
    Process a json object with GDAL raster operations.
    @return: An array with the processed files.
    """
    log.setLevel(loglevel)
    try:
        source_path = obj["source_path"]
        process = obj["process"]
    except Exception:
        pass
        log.error("Raise exception: output_path, source_path and process type are mandatory")
    output_path = obj["output_path"] if "output_path" in obj else None
    output_file_name = obj["output_file_name"] if "output_file_name" in obj else str(uuid.uuid4())
    if output_path is not None and not os.path.isdir(output_path):
        os.makedirs(output_path)
    band = obj["band"] if "band" in obj else 1

    # deal with pixel size
    pixel_size = None

    # Processing
    p = Process(output_file_name)

    # default init is the source_path
    output_processed_files = source_path
    # looping throught processes
    for process_values in process:
        for key in process_values:
            if key in key_function:
                # explicit functions
                if "extract_bands" in key:
                    output_processed_files = p.extract_bands(output_processed_files, band, output_path)
                # get the pixel size
                elif "get_pixel_size" in key:
                    pixel_size = p.get_pixel_size(output_processed_files[0], process_values[key])
                    log.info(pixel_size)
            else:
                # Standard GDAL functions
                process_values[key] = change_values(process_values[key], pixel_size)
                # reflection methods calls
                output_processed_files = getattr(p, key)(process_values[key], output_processed_files, output_path)
    return output_processed_files


def change_values(obj, pixel_size):
    s = json.dumps(obj)
    s = s.replace("{{PIXEL_SIZE}}", str(pixel_size))
    return json.loads(s)


# Class to process using reflection
class Process:

    def __init__(self, output_file_name=None):
        if output_file_name is not None:
            self.output_file_name = output_file_name

    def extract_bands(self, input_files, band, output_path):
        file_bands = []
        filenames = []
        ext = None
        try:
            files = input_files
            for f in files:
                gtif = gdal.Open(f)
                sds = gtif.GetSubDatasets()
                file_bands.append(sds[int(band) - 1][0])
                filenames.append(get_filename(f))
                if ext is None:
                    filename, ext = os.path.splitext(f)
            return self.extract_band_files(file_bands, filenames, output_path, ext)
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def extract_band_files(self, input_file_bands, input_filenames, output_path, ext=None):
        output_files = []
        i = 0
        try:
            for file_band, filename in zip(input_file_bands, input_filenames):
                output_file_path = os.path.join(output_path, filename)
                cmd = "gdal_translate '" + file_band + "' " + output_file_path
                log.info(cmd)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, error = process.communicate()
                log.info(output)
                output_files.append(output_file_path)
                i += 1
            return output_files
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def get_pixel_size(self, input_file, formula=None):
        # TODO: get pixel value with rasterio library?
        cmd = "gdalinfo " + input_file + " | grep Pixel"
        log.info(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            log.info(output)
            if "Pixel Size" in output:
                pixel_size = output[output.find("(")+1:output.find(",")]
                log.info(pixel_size)
                formula = formula.replace("{{PIXEL_SIZE}}", str(pixel_size))
                log.info(formula)
                return eval(formula)
            return None
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def gdal_merge(self, parameters, input_files, output_path):
        output_files = []
        output_file = os.path.join(output_path, self.output_file_name)
        output_files.append(output_file)
        cmd = "gdal_merge.py "
        if "opt" in parameters:
            for key in parameters["opt"].keys():
                cmd += " " + key + " " + str(parameters["opt"][key])
        for input_file in input_files:
            cmd += " " + input_file
        cmd += " -o " + output_file
        log.info(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            log.info(output)
            return output_files
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def gdalwarp(self, parameters, input_files, output_path):
        output_files = []
        output_file = os.path.join(output_path, self.output_file_name)
        output_files.append(output_file)
        cmd = "gdalwarp "
        if "opt" in parameters:
            for key in parameters["opt"].keys():
                cmd += " " + key + " " + str(parameters["opt"][key])
        for input_file in input_files:
            cmd += " " + str(input_file)
        cmd += " " + output_file
        log.info(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            log.info(output)
            return output_files
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def gdal_translate(self, parameters, input_files, output_path):
        output_files = []
        output_file = os.path.join(output_path, self.output_file_name)
        output_files.append(output_file)
        cmd = "gdal_translate "
        if "opt" in parameters:
            for key in parameters["opt"].keys():
                cmd += " " + key + " " + str(parameters["opt"][key])
        for input_file in input_files:
            cmd += " " + input_file
        cmd += " " + output_file
        log.info(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            log.info(output)
            return output_files
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)

    def gdaladdo(self, parameters, input_files, output_path=None):
        output_files = []
        cmd = "gdaladdo "
        for key in parameters["parameters"].keys():
            cmd += " " + key + " " + str(parameters["parameters"][key])
        for input_file in input_files:
            cmd += " " + input_file
            output_files.append(input_file)
        cmd += " " + parameters["overviews_levels"]
        log.info(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            log.info(output)
            return output_files
        except Exception, e:
            log.error(e)
            raise Exception(e, 400)


def callMethod(o, name, options, input_files):
    getattr(o, name)(options, input_files)


def get_filename(filepath):
    drive, path = os.path.splitdrive(filepath)
    path, filename = os.path.split(path)
    return os.path.splitext(filename)[0]