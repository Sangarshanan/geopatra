"""Folium Heatmap Plot."""

from folium.plugins import HeatMap
from .utils import _folium_map


def heatmap(
    df,
    weight=None,
    width=950,
    height=550,
    location=None,
    zoom=7,
    tiles="OpenStreetMap",
    attr=None,
    style={},
):
    """
    Plot a Heatmap out of a geodataframe.

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
    gpd_copy = df.copy()
    col = gpd_copy._geometry_column_name
    lon = [lon.x for lon in gpd_copy[col]]
    lat = [lat.y for lat in gpd_copy[col]]
    if weight:
        max_weight = float(gpd_copy[weight].max())
        style["max_val"] = max_weight
        data = list(zip(lat, lon, gpd_copy[weight]))
    else:
        data = list(zip(lat, lon))
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )

    HeatMap(data, **style).add_to(m)
    return m
