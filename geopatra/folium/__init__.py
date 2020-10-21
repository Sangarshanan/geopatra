# flake8: noqa

from .geojson import geojson
from .circle import circle
from .choropleth import choropleth
from .markercluster import markercluster
from .heatmap import heatmap

# module level doc-string
__doc__ = """
Interactive maps with folium
=============================
Build an interface for geodataframes to work natively with Folium 
Supported Maps
-------------
  - Geojson plots (Just plot the geometries in geodataframes)
  - Choropleth maps
  - Markercluster (Count, Sum, Average)
  - Heatmaps 
"""
