# flake8: noqa

from .geojson import geojson
from .circle import circle
from .chloropeth import chloropeth
from .markercluster import markercluster
from .heatmap import heatmap

from .main import FoliumMap

# module level doc-string
__doc__ = """
Interactive maps with Folium
=============================
Interface for geodataframes to work natively with Folium 
Supported Map kinds
-------------
  - Default geojson plots (Just plot the geometries in geodataframes)
  - Circle plots (Points as circles)
  - Markercluster (Count, Sum, Average)
  - Heatmaps
"""
