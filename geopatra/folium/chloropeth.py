"""Folium chloropeth Plot."""

import folium
from .utils import _get_color_map, _folium_map, _get_tooltip, _random_string


def chloropeth(
    gdf,
    color_by,
    index_col=None,
    legend=None,
    name="layer",
    width=950,
    height=550,
    location=None,
    color="blue",
    tooltip=None,
    zoom=11,
    tiles="OpenStreetMap",
    attr=None,
    style={},
):
    """
    Plot a Chloropeth map out of a geodataframe.

    Parameters
    ----------
    gdf : GeoDataframe
    color_by : Column name used to color the geometries
    index_col : Index column or the primary key column, optional
                index is created if it is not specified
    legend : String, legend caption used to create one on the top right
            default None (No legend)
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
    colormap = _get_color_map(color, legend, gpd_copy, color_by)
    if not index_col:
        object_col = "index_{}".format(_random_string(4))
        gpd_copy[object_col] = range(0, len(gpd_copy))
    else:
        object_col = index_col
    layer_dict = gpd_copy.set_index([object_col])[color_by]
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    color_dict = {key: colormap(layer_dict[key]) for key in layer_dict.keys()}
    folium.GeoJson(
        gpd_copy.__geo_interface__,
        name=name,
        tooltip=folium.GeoJsonTooltip(fields=_get_tooltip(tooltip, gpd_copy)),
        style_function=lambda feature: {
            "fillColor": color_dict[feature["properties"][object_col]],
            **style,
        },
    ).add_to(m)
    folium.LayerControl().add_to(m)
    if legend:
        colormap.add_to(m)
    return m
