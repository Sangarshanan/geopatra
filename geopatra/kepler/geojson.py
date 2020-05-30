"""Kepler geojson Plot."""

import os
import ast
import json
from jinja2 import Template
from keplergl import KeplerGl

from . import module_path
from .utils import random_char

field_types = {"int64": "integer", "float64": "real", "object": "string"}


def geojson(gdf, height=400, name="layer", **kwargs):
    """
    Convert Geodataframe to geojson and plot it.

    Parameters
    ----------
    gdf : GeoDataframe
    height : Height of the plot. default: 400
    name : name of the layer. default: 'layer'
    tooltip: tooltips shown in the map. eg: ['continent', 'pop_est'],
    color: color of the rendered geometries eg: [255,0,0],
    opacity: opacity of the rendered geometries eg: 0.1,
    stroke_color: stroke color of the rendered geometries eg: [0,0,0],
    stroke_thickness: stroke thickness of the rendered geometries eg: 1,
    color_field: field to base the color on eg: 'pop_est',
    color_scheme: color scheme for the geometries colored
    based on color_field eg: 'Blues', list of available color schemes:
    https://gist.github.com/jsundram/6004447#file-colorbrewer-json
    color_scheme_steps: Steps available in color schemes eg: 3-9,10,11,12

    Returns
    -------
    map : keplergl.keplergl.KeplerGl
    """
    config_path = os.path.join(module_path, "config", "geojson.config")
    # Set Default Layername and Height
    kwargs.update({"height": height, "name": name})
    if "color_field" in kwargs:
        col_type = str(gdf[kwargs["color_field"]].dtype)
        kwargs.update({"color_field_type": field_types[col_type]})
    if "color_scheme" in kwargs:
        colorbrewer_path = os.path.join(module_path, "config", "colors.json")
        with open(colorbrewer_path) as f:
            colorbrewer = json.load(f)
        color_scheme = kwargs["color_scheme"]
        steps = kwargs.setdefault("color_scheme_steps", 6)
        colors = colorbrewer[color_scheme][str(steps)]
        kwargs.update({"colorbrewer": colors})
    with open(config_path, "r") as f:
        t = Template(f.read())
        config = ast.literal_eval(t.render(kwargs, id_=random_char(6)))
    map_ = KeplerGl(height=height, data={name: gdf}, config=config)
    return map_
