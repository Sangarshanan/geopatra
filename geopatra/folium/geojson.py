"""Folium geojson Plot."""

import folium
from .utils import (
    _random_color_hex,
    _folium_map,
    _get_tooltip,
    _random_string,
    _get_color_map,
)


def geojson(
    gdf,
    color_by=None,
    name="layer",
    width="100%",
    height="100%",
    location=None,
    color="blue",
    tooltip=None,
    index_col=None,
    legend=None,
    zoom=7,
    tiles="OpenStreetMap",
    attr=None,
    style={},
):
    """
    Convert Geodataframe to geojson and plot it.

    Parameters
    ----------
    gdf : GeoDataframe
    name : name of the geojson layer, optional, default "layer"
    width : width of the map, default 950
    height : height of the map, default 550
    location : center of the map rendered, default centroid of first geometry
    color : color of your geometries, default blue
            use random to randomize the colors
    tooltip : hover box on the map with geometry info, default all columns
            can be a list of column names
    zoom : zoom level of the map, default 7
    tiles : basemap, default openstreetmap,
            options ['google','googlesatellite','googlehybrid'] or custom wms
    attr : Attribution to external basemaps being used, default None
    style : dict, additional style to geometries
    Returns
    -------
    m : folium.map
    """
    gpd_copy = gdf.copy()
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    color_column = "color{}".format(_random_string(4))
    if isinstance(color, list):
        gpd_copy[color_column] = color
    elif color.lower() == "random":
        gpd_copy[color_column] = _random_color_hex(len(gdf))
    else:
        gpd_copy[color_column] = [color] * len(gpd_copy)
    if color_by is not None:
        colormap = _get_color_map(color, legend, gpd_copy, color_by)
        if not index_col:
            object_col = "index_{}".format(_random_string(4))
            gpd_copy[object_col] = range(0, len(gpd_copy))
        else:
            object_col = index_col
        layer_dict = gpd_copy.set_index([object_col])[color_by]
        color_dict = {key: colormap(layer_dict[key]) for key in layer_dict.keys()}
        folium.GeoJson(
            gpd_copy.to_json(),
            name=name,
            tooltip=_get_tooltip(tooltip, gpd_copy),
            style_function=lambda feature: {
                "fillColor": color_dict[feature["properties"][object_col]],
                **style,
            },
        ).add_to(m)
        folium.LayerControl().add_to(m)
        if legend:
            colormap.add_to(m)
    else:
        folium.GeoJson(
            gpd_copy.to_json(),
            tooltip=_get_tooltip(tooltip, gdf),
            style_function=lambda x: {"color": x["properties"][color_column], **style},
            name=name,
        ).add_to(m)
    return m
