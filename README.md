![alt text](https://github.com/Sangarshanan/geopatra/blob/master/docs/_static/geopatra.png "Geopatra")


[![Documentation Status](https://readthedocs.org/projects/geopatra/badge/?version=latest)](https://geopatra.readthedocs.io/en/latest/?badge=latest)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/sangarshanan/geopatra/issues) [![image](https://img.shields.io/pypi/v/geopatra.svg)](https://pypi.org/project/geopatra/) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)



> :warning: **This package is still an early protoype**: Will be working on making it better, beware of bad code  


Create Interactive maps 🗺️ with your geodataframe

Geopatra attempts to wrap the goodness of Folium, Plotly, Kepler.gl and maybe even more amazing libraries for rapidly creating interactive maps with Geodataframes


## Installation 

Everything is always a pip away

```
pip install geopatra
```

## Basic Usage

To quickly plot a geodataframe with folium 

```
import geopatra
import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
m = world.folium.plot()
```
Now you have a folium map object, which you can now use for more complex mapflows 

Check out [docs](https://geopatra.readthedocs.io/en/latest/geopatra.html) for more examples

## Development 

This package uses the awesome [poetry](https://github.com/python-poetry/poetry)

```
git clone git@github.com:Sangarshanan/geopatra.git
poetry install
```

## TODO

- Clean up existing code 
- Add more folium maps
- Try to set up similar flows with plotly express and Kepler.gl

