import os
import qgis.core as qgc
#from qgis import processing

def clip_raster_by_vector(input_raster, input_vector, output_raster):

    params = {'ALPHA_BAND': False,
              'CROP_TO_CUTLINE': True,
              'DATA_TYPE': 0,
              'EXTRA': '',
              'INPUT': name_of_tif,
              'KEEP_RESOLUTION': False,
              'MASK': name_of_shape,
              'MULTITHREADING': False,
              'NODATA': None,
              'OPTIONS': '',
              'OUTPUT': output_raster,
              'SET_RESOLUTION': False,
              'SOURCE_CRS': None,
              'TARGET_CRS': None,
              'X_RESOLUTION': None,
              'Y_RESOLUTION': None}

    feedback = qgc.QgsProcessingFeedback()
    alg_name = 'gdal:cliprasterbymasklayer'
    # print(processing.algorithmHelp(alg_name))
    result = processing.run(alg_name, params, feedback=feedback)
    return result

def clip_raster_by_extent(xul, yul, xlr, ylr, projection, input_raster, output_raster):
    print('{},{},{},{} [{}]'.format(xul, xlr, ylr, yul, projection))

    params = {'DATA_TYPE': 0,
              'EXTRA': '',
              'INPUT': input_raster,
              'NODATA': None,
              'OPTIONS': '',
              'OUTPUT': output_raster,
              'OVERCRS': False,
              'PROJWIN': '{},{},{},{} [{}]'.format(xul, xlr, ylr, yul, projection)}

    feedback = qgc.QgsProcessingFeedback()
    alg_name = 'gdal:cliprasterbyextent'
    # print(processing.algorithmHelp(alg_name))
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
    name_of_tif = "{}25m_fusion.tif".format(path_to_tif)
    display_name = "dem"
    rlayer = qgc.QgsRasterLayer(name_of_tif, display_name)
    if not rlayer.isValid():
        print("Raster layer failed to load!")
    qgc.QgsProject.instance().addMapLayer(rlayer)

    # load shapefile for crop
    path_to_shape = "./remaud/catchment-shapefile/"
    name_of_shape = "{}Bassin_Versant.shp".format(path_to_shape)
    display_name = "crop"
    vlayer = qgc.QgsVectorLayer(name_of_shape, display_name)
    if not vlayer.isValid():
        print("Vector layer failed to load!")
    qgc.QgsProject.instance().addMapLayer(vlayer)

    # crop the DEM
    cropped_raster = "{}dem_cropped.tif".format(path_to_tif)
    result = clip_raster_by_vector(name_of_tif, name_of_shape, cropped_raster)
    print(f'crop result = {result}')

    # calculate extent of cropped DEM
    display_name = "cropped_dem"
    rlayer = qgc.QgsRasterLayer(cropped_raster, display_name)
    if not rlayer.isValid():
        print("Raster layer failed to load!")
    qgc.QgsProject.instance().addMapLayer(rlayer)

    layer = qgc.QgsProject.instance().mapLayersByName('cropped_dem')[0]
    extent = layer.extent()
    print(extent)

    # chop of the bottom to the Pont Napolean III
    xul = extent.xMinimum()
    yul = extent.yMaximum()
    xlr = extent.xMaximum()
    ylr = 6293963.0370555185  # latitude to cut at
    projection = 'EPSG:2154'

    clipped_raster = "{}dem_clipped.tif".format(path_to_tif)
    result = clip_raster_by_extent(xul, yul, xlr, ylr, projection, cropped_raster, clipped_raster)
    print(f'clip result = {result}')

    # Finally, exitQgis() is called to remove the
    # provider and layer registries from memory
    qgs.exitQgis()

    # tidy up
    os.remove(cropped_raster)