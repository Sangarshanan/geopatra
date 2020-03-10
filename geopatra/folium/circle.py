"""Folium markercluster Plot."""

import folium
from .utils import _get_lat_lon, _folium_map, _get_tooltip


def circle(
    gdf,
    radius=10,
    fill=True,
    fill_color=None,
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
    radius: radius of the circle
    fill: fill the circle
    fill_color: fill the circle with this color (column name or color)
    name : name of the geojson layer, optional, default "layer"
    width : width of the map, default 950
    height : height of the map, default 550
    location : center of the map rendered, default centroid of first geometry
    color : color of your geometries, default blue
            use random to randomize the colors (column name or color)
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
    ignore_col = ["latitude", "longitude"]
    gpd_copy = _get_lat_lon(gdf.copy())
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    tooltip_cols = _get_tooltip(tooltip, gpd_copy, ignore_col)
    for index, row in gpd_copy.iterrows():
        tooltip_dict = {k: v for k, v in dict(row).items() if k in tooltip_cols}
        tooltip = "".join(
            [
                "<p><b>{}</b> {}</p>".format(keyvalue[0], keyvalue[1])
                for keyvalue in list(tooltip_dict.items())
            ]
        )
        if fill_color in list(gpd_copy.columns):
            fill_color = row[fill_color]
        if color in list(gpd_copy.columns):
            color = row[color]
        folium.Circle(
            radius=radius,
            location=[row["latitude"], row["longitude"]],
            tooltip=tooltip,
            popup=tooltip,
            fill=fill,
            color=color,
            fill_color=fill_color,
        ).add_to(m)

    return m
