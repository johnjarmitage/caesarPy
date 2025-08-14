import os
import sys
import qgis.core as qgc
#from qgis import processing

def resample(input_raster, output_raster, resolution, method):

    params = { 'DATA_TYPE' : 0,
               'EXTRA' : '',
               'INPUT' : input_raster,
               'MULTITHREADING' : False,
               'NODATA' : None,
               'OPTIONS' : '',
               'OUTPUT' : output_raster,
               'RESAMPLING' : method,
               'SOURCE_CRS' : None,
               'TARGET_CRS' : None,
               'TARGET_EXTENT' : None,
               'TARGET_EXTENT_CRS' : None,
               'TARGET_RESOLUTION' : resolution }

    feedback = qgc.QgsProcessingFeedback()
    alg_name = "gdal:warpreproject"
    #print(processing.algorithmHelp(alg_name))
    result = processing.run(alg_name, params, feedback=feedback)
    return result


if __name__ == '__main__':

    res = sys.argv[1]
    
    # Supply path to qgis install location
    qgc.QgsApplication.setPrefixPath("/work/armitagj/nminiconda3/envs/qgis_stable", True)

    # Create a reference to the QgsApplication.  Setting the
    # second argument to False disables the GUI.
    qgs = qgc.QgsApplication([], False)

    # Load providers
    qgs.initQgis()

    # Load the processing toolbox
    from qgis import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # Write your code here to load some layers, use processing
    # algorithms, etc.

    # load DEM
    name_of_tif =  sys.argv[2]
    display_name = "dem"
    rlayer = qgc.QgsRasterLayer(name_of_tif, display_name)
    if not rlayer.isValid():
        print("Raster layer failed to load!")
    qgc.QgsProject.instance().addMapLayer(rlayer)
    
    layer = qgc.QgsProject.instance().mapLayersByName('dem')[0]
    extent = layer.extent()
    print(extent)

    # resample mean
    resampled_raster = '{}_{}m_mean.tif'.format(name_of_tif.split('.')[0], res)
    resolution = res
    method = 5
    """
    0 — Nearest neighbour
    1 — Bilinear
    2 — Cubic
    3 — Cubic spline
    4 — Lanczos windowed sinc
    5 — Average
    6 — Mode
    7 — Maximum
    8 — Minimum
    9 — Median
    10 — First quartile
    11 — Third quartile
    """
    result = resample(name_of_tif, resampled_raster, resolution, method)
    print(f'Resample result = {result}')

    # resample minimum
    resampled_raster = '{}_{}m_min.tif'.format(name_of_tif.split('.')[0], res)
    resolution = res
    method = 8
    """
    0 — Nearest neighbour
    1 — Bilinear
    2 — Cubic
    3 — Cubic spline
    4 — Lanczos windowed sinc
    5 — Average
    6 — Mode
    7 — Maximum
    8 — Minimum
    9 — Median
    10 — First quartile
    11 — Third quartile
    """
    result = resample(name_of_tif, resampled_raster, resolution, method)
    print(f'Resample result = {result}')

    # Finally, exitQgis() is called to remove the
    # provider and layer registries from memory
    qgs.exitQgis()
