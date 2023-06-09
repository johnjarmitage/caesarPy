"""
test ceasarpy/demio.py asc2numpy
John J Armitage
"""

import os, sys
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import caesarpy as cp

if __name__ == '__main__':
    dem_asc = 'test.asc'
    print(dem_asc)
    nx, ny, geotransform, dem = cp.demio.asc2numpy(dem_asc)
    print(f'DEM has dimensions {nx}, {ny}')