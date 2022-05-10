## A bunch of useful functions for dealing with the input and output of [HAIL-CAESAR](https://github.com/dvalters/HAIL-CAESAR)

`tif2asc`: To convert a tif raster image to ascii raster format.

`tif2asc_resample`: To convert and downsample a tif raster image to ascii raster format.

`asc2numpy`: To load an ascii raster file into a numpy array. (xarray would be cooler)

## A bunch of notebooks to explore the input and output of HAIL-CAESAR

---

## A wee presentation for EGU 2022

A notebook as a presentation of course: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/johnjarmitage/caesarPy/HEAD?labpath=notebooks%2FEGU2022%2Fpresentation.ipynb)]

---

### Create the environment

First fork and clone the files to your computer. Then using either [`conda`](https://docs.conda.io/en/latest/miniconda.html) or [`mamba`](https://mamba.readthedocs.io/en/latest/) create the Python environment in the terminal:

```
mamba env create -f path/to/environment.yml
conda activate caesarpy 
```
Launch `jupyter_lab` and modify the files as needed.

### Keeping your forked version up-to-date

Once you have forked and cloned the repo onto your computer in the terminal make git aware that there is an upstream repository:

```
cd path/to/caesarPy
git remote add upstream git://github.com/johnjarmitage/caesarPy.git
git fetch upstream
```
Subsequently to update your local copy:
```
git pull upstream master
```
This will pull the upstream version into your computer. You can then push this to the forked copy of the repository in your github account:
```
git push origin master
```
before or after you have found all the mistakes...


