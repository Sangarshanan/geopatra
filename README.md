![alt text](https://github.com/Sangarshanan/geopatra/blob/master/docs/_static/geopatra.png "Geopatra")

![Travis (.org)](https://img.shields.io/travis/sangarshanan/geopatra?label=travis&logo=travis) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/sangarshanan/geopatra/Test?label=actions&logo=github) [![Documentation Status](https://readthedocs.org/projects/geopatra/badge/?version=latest)](https://geopatra.readthedocs.io/en/latest/?badge=latest) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geopatra) [![image](https://img.shields.io/pypi/v/geopatra.svg)](https://pypi.org/project/geopatra/) 



Create Interactive maps 🗺️ with your geodataframe

Geopatra attempts to wrap the goodness of Folium, Plotly, Kepler.gl and maybe even more amazing libraries (Bokeh, Altair) for rapidly creating interactive maps with Geodataframes

You can already create interactive maps easily with geopandas and Folium/ Plotly/ Kepler.gl. Geopatra is merely meant to make this easier and is more geared towards ease and currently does not support complex maps or intricate style control


## Installation 

Everything is always a pip away

```
pip install geopatra
```

## Basic Usage

To quickly plot a geodataframe with folium, you gotta understand workflows in geopandas and folium.

```python
import folium
import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
m = folium.Map(location = [4,10], zoom_start = 3)
folium.GeoJson(world.__geo_interface__).add_to(m)
```

With Geopatra all the parameters you set with folium become optional so you don't have to care about folium   

```python
import geopatra
m = world.folium.plot()
```
Now you have a folium map object, which you can now use for more complex mapflows 

Check out [docs](https://geopatra.readthedocs.io/en/latest/geopatra.html) for more examples

## Development 

Clone the repo
```git
git clone git@github.com:Sangarshanan/geopatra.git
```

Run ```pre-commit install``` to install pre-commit into your git hooks. pre-commit will now run on every commit

Install the package with the amazing [poetry](https://github.com/python-poetry/poetry)

```
poetry install
```

Make the bla-bla-bla changes to code and run the tests, Once merged to master build and publish

```
poetry build
poetry publish
```

