from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksProcessing',
    version='0.0.2',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks processing library for raster data.',
    install_requires=[
        'flask', 'BeautifulSoup'
    ],
    url='http://pypi.python.org/pypi/GeobricksProcessing/',
    keywords=['geobricks', 'processing', 'raster', 'gis', 'gdal']
)
