"""Folium Utilities."""

import random
import string
import folium
from branca.colormap import linear


def _folium_map(gpd_copy, width, height, location, tiles, attr, zoom_start):
    """Create a base folium map."""
    if tiles.lower() == "google":
        tiles = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
        if attr is None:
            attr = "google.com Roads"
    elif tiles.lower() == "googlesatellite":
        tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        if attr is None:
            attr = "google.com Satellite"
    elif tiles.lower() == "googlehybrid":
        tiles = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
        if attr is None:
            attr = "google.com Hybrid"
    if location is None:
        col = gpd_copy._geometry_column_name
        location = list(reversed(list(gpd_copy.iloc[0][col].centroid.coords[0])))
    m = folium.Map(
        width=width,
        height=height,
        location=location,
        tiles=tiles,
        attr=attr,
        zoom_start=zoom_start,  # Limited levels of zoom for free Mapbox tiles.
    )
    return m


def _random_color_hex(n):
    """Randomize Color."""
    colors = []
    for i in range(n):
        colors.append("#{:06x}".format(random.randint(0, 0xFFFFFF)))
    return colors


def _get_tooltip(tooltip, gpd, ignore_col=None):
    """Show everything or columns in the list."""
    if tooltip is None:
        tooltip = list(gpd.__geo_interface__["features"][0]["properties"].keys())
    if ignore_col:
        tooltip = [
            tooltip_column
            for tooltip_column in tooltip
            if tooltip_column not in tuple(ignore_col)
        ]
    return tooltip


def _get_color_map(color, legend, gpd, color_by):
    """Color geometries."""
    max_val = gpd[color_by].max()
    min_val = gpd[color_by].min()
    if color == "green" or color is None:
        colormap = linear.YlGn_09.scale(min_val, max_val)
    elif color == "red":
        colormap = linear.OrRd_09.scale(min_val, max_val)
    elif color == "blue":
        colormap = linear.PuBu_09.scale(min_val, max_val)
    else:
        colormap = color

    if legend:
        colormap.caption = legend
    return colormap


def _get_lat_lon(df):
    """Get latitude and longitude from geometries."""
    col = df._geometry_column_name
    df["latitude"] = [latlon.y for latlon in df[col]]
    df["longitude"] = [latlon.x for latlon in df[col]]
    return df


def _random_string(length):
    """Generate random string."""
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return res
