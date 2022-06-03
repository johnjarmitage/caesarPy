# Pre-processing a DEM for landscape evolution modelling

A DEM will come with artifacts and imperfections that will cause barriers for the overland flow model in landscape evolution models. It is likewise probable that the original DEM resolution will be too high for the LEM, so resampling of the DEM will bring in artifacts that will also impact the model. Here, I will outline the steps developed by Arthur Remaud during his apprenticeship at IFPEN.

We resample the original DEM at a lower resolution using the mean elevation and the minimum elevation. The minimum elevation will better represent the valley floors, while the mean gives a better representation of the hypsometery of the catchment. We therefore use the minimum DEM to replace the mean DEM within the channels. Channels are found using a D4 routing algorithm, because we will model landscape evolution using CAESAR-Lisflood and this code likewise uses a D4 algorithm.

Key dependencies are:

* `Qgis` that we use for manipulating the DEM. However, `Qgis` is not the only code that can do what we need.
* `landlab` and in particular the D4 routing algorithm

