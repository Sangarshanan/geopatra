"""Folium geojson Plot."""

import folium
from .utils import _random_color_hex, _folium_map, _get_tooltip, _random_string


def geojson(
    gdf,
    name="layer",
    width=950,
    height=550,
    location=None,
    color="blue",
    tooltip=None,
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
    color_column = "color{}".format(_random_string(4))
    if isinstance(color, list):
        gpd_copy[color_column] = color
    elif color.lower() == "random":
        gpd_copy[color_column] = _random_color_hex(len(gdf))
    else:
        gpd_copy[color_column] = [color] * len(gpd_copy)

    geo_json = gpd_copy.__geo_interface__

    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    folium.GeoJson(
        geo_json,
        tooltip=folium.GeoJsonTooltip(
            fields=_get_tooltip(tooltip, gpd_copy, color_column)
        ),
        style_function=lambda x: {"color": x["properties"][color_column], **style},
        name=name,
    ).add_to(m)
    return m
