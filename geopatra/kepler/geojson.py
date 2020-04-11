"""Kepler geojson Plot."""

import os
import ast
from jinja2 import Template
from keplergl import KeplerGl

from . import module_path
from .utils import random_char


def geojson(
    gdf,
    name,
    tooltip=None,
    fill_color=None,
    fill_opacity=None,
    stroke_color=None,
    stroke_thickness=None,
    height=400,
):
    config_path = os.path.join(module_path, "config", "geojson.config")
    with open(config_path, "r") as f:
        t = Template(f.read())
        config = ast.literal_eval(
            t.render(
                id_=random_char(6),
                name=name,
                tooltip=tooltip,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_thickness=stroke_thickness,
            )
        )
    map_ = KeplerGl(height=height, data={name: gdf}, config=config)
    return map_
