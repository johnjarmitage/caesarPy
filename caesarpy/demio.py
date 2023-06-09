"""
functions for DEM input and output preparation for use with HAIL-CAESAR
John J Armitage
"""

from osgeo import gdal
import numpy as np
import rasterio as rio
from scipy.interpolate import RegularGridInterpolator


def tif2asc(tiffile, ascfile):
    """
    Function to convert a geotiff (.tif) file into an ascii file (.asc)
    :param tiffile: input geotiff file name
    :param ascfile: output ascii file name (CAESAR expects .asc)
    :return: None
    """
    rio_array = rio.open(tiffile)  # read in tif file
    data_array = rio_array.read(1).astype(float)  # assume that elevation is in the first band

    f = open(ascfile, 'w')
    f.write('ncols         {}\n'.format(np.shape(data_array)[1]))
    f.write('nrows         {}\n'.format(np.shape(data_array)[0]))
    f.write('xllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[0]))
    f.write('yllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[1]))
    f.write('cellsize      {}\n'.format(rio_array.transform[0]))
    f.write('NODATA_value  -9999\n')

    pix = '{0} '
    for i in range(np.shape(data_array)[0]):
        for j in range(np.shape(data_array)[1]):
            if np.isnan(data_array[i, j]) == True:
                f.write(pix.format(np.int(-9999)))  # need to replace nan with -9999
            else:
                f.write(pix.format(data_array[i, j]))
        f.write("\n")
    f.close()


def tif2asc_resample(tiffile, ascfile, outdxy, cut):
    """
    Function to resample the input tif and output as ascii ready for CAESAR
    :param tiffile: input geotiff file name
    :param ascfile: output ascii file name (CAESAR expects .asc)
    :param outdxy: output DEM cell size
    :param cut: number of cells to cut off the top to create an outflow
    :return: None
    """
    rio_array = rio.open(tiffile)  # read in tif file
    in_array = rio_array.read(1).astype(float)  # assume that elevation is in the first band
    in_array[in_array <= 0] = np.nan  # replace -9999 with nan

    indxy = rio_array.transform[0]  # cell size of input DEM
    print('input cell size is {} m'.format(indxy))
    ny, nx = np.shape(in_array)  # number of cells in x and y (cols and rows)
    x = np.linspace(0, indxy * nx, nx)
    y = np.linspace(0, indxy * ny, ny)

    ny = np.int((indxy * ny) / outdxy)  # number of cells in new output DEM
    nx = np.int((indxy * nx) / outdxy)
    outx = np.linspace(0, outdxy * nx, nx)
    outy = np.linspace(0, outdxy * ny, ny)
    outX, outY = np.meshgrid(outx, outy)  # new grid of x and y coordinates
    print('output cell size is {} m'.format(outX[0, 1] - outX[0, 0]))

    resample = RegularGridInterpolator((y, x), in_array)  # use the scipy RegularGridInterpolator to resample the DEM
    pts = np.stack((np.ravel(outY), np.ravel(outX)), axis=-1)  # points to resample to
    data_vector = resample(pts)  # output DEM vector
    data_array = data_vector.reshape(np.int(ny), np.int(nx))  # ouput DEM array
    cut_array = data_array[cut:, :]  # cut of the top [0, :] of the DEM to make outflow point

    f = open(ascfile, 'w')  # output DEM array to asc file for CAESAR to play with
    f.write('ncols         {}\n'.format(np.shape(cut_array)[1]))
    f.write('nrows         {}\n'.format(np.shape(cut_array)[0]))
    f.write('xllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[0]))
    f.write('yllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[1]))
    f.write('cellsize      {}\n'.format(outdxy))
    f.write('NODATA_value  -9999\n')

    pix = '{0} '
    for i in range(np.shape(cut_array)[0]):
        for j in range(np.shape(cut_array)[1]):
            if np.isnan(cut_array[i, j]) == True:
                f.write(pix.format(np.int(-9999)))  # need to replace nan with -9999
            else:
                f.write(pix.format(cut_array[i, j]))
        f.write("\n")
    f.close()


def asc2numpy(ascfile):
    """
    Function to read in an ascii file (.asc) and return a Numpy array
    :param ascfile: input ascii file name
    :return ncols: number of columns
    :return nrows: number of rows
    :return geotransform: the geo-transfrom info
    :return data: a numpy array of the ascii data
    """

    try:
        gdal_data = gdal.Open(ascfile)  # use GDAL to open the ascii fle
        ncols = gdal_data.RasterXSize  # get the number of columns
        nrows = gdal_data.RasterYSize  # get the number of rows
        geotransform = gdal_data.GetGeoTransform()  # get the geo-transform info
        data_array = gdal_data.ReadAsArray().astype(np.float)  # convert the data into a numpy array
        data_array[data_array <= -9999] = np.nan  # replace -9999 with nan

        return ncols, nrows, geotransform, data_array

    except:
        print('cannot open {}'.format(ascfile))

        
def numpy2asc(array, tiffile, ascfile):
    """
    Function to convert a geotiff (.tif) file into an ascii file (.asc)
    :param tiffile: input geotiff file name
    :param ascfile: output ascii file name (CAESAR expects .asc)
    :return: None
    """
    rio_array = rio.open(tiffile)  # read in tif file
    
    f = open(ascfile, 'w')
    f.write('ncols         {}\n'.format(np.shape(array)[1]))
    f.write('nrows         {}\n'.format(np.shape(array)[0]))
    f.write('xllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[0]))
    f.write('yllcorner     {}\n'.format((rio_array.transform * (0, rio_array.height))[1]))
    f.write('cellsize      {}\n'.format(rio_array.transform[0]))
    f.write('NODATA_value  -9999\n')

    pix = '{0} '
    for i in range(np.shape(array)[0]):
        for j in range(np.shape(array)[1]):
            if np.isnan(array[i, j]) == True:
                f.write(pix.format(int(-9999)))  # need to replace nan with -9999
            elif array[i, j] <= 0:
                f.write(pix.format(int(-9999)))  # need to replace 0 with -9999
            else:
                f.write(pix.format(array[i, j]))
        f.write("\n")
    f.close()
    

def asc2xyz(ascfile):
    """
    Function to read in an ascii file (.asc) and return Numpy arrays of X, Y and Z
    :param ascfile: input ascii file name
    :return X : a numpy array of x-coordinates
    :return Y : a numpy array of y-coordinates
    :return Z : a numpy array of the ascii data
    """

    try:
        gdal_data = gdal.Open(ascfile)  # use GDAL to open the ascii fle
        nx = gdal_data.RasterXSize  # get the number of columns
        ny = gdal_data.RasterYSize  # get the number of rows
        geotransform = gdal_data.GetGeoTransform()  # get the geo-transform info
        ll = (geotransform[0], geotransform[3] + ny * geotransform[5])  # lower left corner
        ul = (geotransform[0], geotransform[3])   # upper left corner
        dx = geotransform[1]
        dy = geotransform[5]
        Z = gdal_data.ReadAsArray().astype(float)  # convert the data into a numpy array
        Z[Z <= -9999] = np.nan  # replace -9999 with nan
        
        x = np.linspace(ll[0], ll[0] + dx * (nx -1), nx)
        y = np.linspace(ul[1], ul[1] + dy * (ny -1), ny)
        X,Y = np.meshgrid(x,y, indexing='xy')

        return X, Y, Z

    except:
        print('cannot open {}'.format(ascfile))


def numpy2asc(array, res, ascfile):
    """
    Function to convert a numpy into an ascii file (.asc)
    :param array: numpy array
    :param res: cell size
    :param ascfile: output ascii file name (CAESAR expects .asc)
    :return: None
    """
    
    f = open(ascfile, 'w')
    f.write('ncols         {}\n'.format(np.shape(array)[1]))
    f.write('nrows         {}\n'.format(np.shape(array)[0]))
    f.write('xllcorner     {}\n'.format(0))
    f.write('yllcorner     {}\n'.format(0))
    f.write('cellsize      {}\n'.format(res))
    f.write('NODATA_value  -9999\n')

    pix = '{0} '
    for i in range(np.shape(array)[0]):
        for j in range(np.shape(array)[1]):
            if np.isnan(array[i, j]) == True:
                f.write(pix.format(int(-9999)))  # need to replace nan with -9999
            elif array[i, j] <= 0:
                f.write(pix.format(int(-9999)))  # need to replace 0 with -9999
            else:
                f.write(pix.format(array[i, j]))
        f.write("\n")
    f.close()