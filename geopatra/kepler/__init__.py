# flake8: noqa

import os

module_path = os.path.dirname(os.path.realpath(__file__))


from .geojson import geojson

# module level doc-string
__doc__ = """
Interactive maps with kepler.gl
=============================
Build an interface for geodataframes to work natively with Kepler.gl 
Supported Maps
-------------
  - Geojson plots (Plot the geometries in geodataframes)
"""
