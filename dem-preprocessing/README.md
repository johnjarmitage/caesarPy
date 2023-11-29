### Pre-processing a DEM for landscape evolution modelling

A DEM will come with artefacts and imperfections that will cause barriers for the overland flow model in landscape evolution models. It is likewise probable that the original DEM resolution will be too high for the LEM, so resampling of the DEM will bring in artefacts that will also impact the model.

We resample the original DEM at a lower resolution using the mean elevation and the minimum elevation. The minimum elevation will better represent the valley floors, while the mean gives a better representation of the hypsometery of the catchment. We therefore use the minimum DEM to replace the mean DEM within the channels. Channels are found using a D4 routing algorithm, because we will model landscape evolution using [`CAESAR-Lisflood`](https://sourceforge.net/projects/caesar-lisflood/) and this code likewise uses a D4 algorithm.

Key dependencies are:

* [`qgis`](https://plugins.qgis.org/planet/tag/conda/) that we use for manipulating the DEM. However, `Qgis` is not the only code that can do what we need.
* [`landlab`](https://landlab.readthedocs.io/en/master/index.html) and in particular the D4 routing algorithm

This directory contains

* `dem-preprocessing*.ipynb` - a notebook that goes through the steps.
* `crop-dem-to-catchment.py` - a python script that uses `Qgis` to crop the DEM to the catchment.
* `resample-dem.py` - a python script that uses `gdal:warp` via `Qgis` to resample the DEM using mean and minimum methods.

The data is too large to be shared here, but at least you get the idea.

To run the python scripts you need to run them in an python environment that has [`qgis`](https://plugins.qgis.org/planet/tag/conda/). For the notebooks that then run the processing, such as the pit filling, they easiest way would be to use the environment [here](../environment.yml).

### Rainfall

A [notebook](./dem-preprocessing-Tet-below-Vinca-Rain.ipynb) is included that calculates regions for spatial rainfall within `CAESAR-lisflood` from the `scipy` nearest neighbour algorithm.

### Population density and soil grain size distribution

Finally two notebooks,

* `population-density-tet.ipynb`
* `soilgrids.ipynb`

are included for the article on microplastic transport that is in submission *watch this space*...