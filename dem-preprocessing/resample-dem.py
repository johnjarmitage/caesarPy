import os
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
    path_to_tif = "./remaud/"
    name_of_tif = "{}dem_clipped.tif".format(path_to_tif)
    display_name = "dem"
    rlayer = qgc.QgsRasterLayer(name_of_tif, display_name)
    if not rlayer.isValid():
        print("Raster layer failed to load!")
    qgc.QgsProject.instance().addMapLayer(rlayer)

    # resample mean
    resampled_raster = '{}dem_200m_mean.tif'.format(path_to_tif)
    resolution = 200
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
    resampled_raster = '{}dem_200m_min.tif'.format(path_to_tif)
    resolution = 200
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
