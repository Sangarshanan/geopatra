"""Different Folium maps."""

import json
import random
import folium
from folium import Marker
from jinja2 import Template
from branca.colormap import linear
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster


def _random_color_hex(n):
    """Randomize Color."""
    colors = []
    for i in range(n):
        colors.append("#{:06x}".format(random.randint(0, 0xFFFFFF)))
    return colors


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


def _get_tooltip(tooltip, gpd):
    """Show everything or columns in the list."""
    if tooltip is None:
        tooltip = list(gpd.__geo_interface__["features"][0]["properties"].keys())
    return tooltip


def _get_color_map(
    color, legend, gpd, color_by,
):
    """Color geometries"""
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


def geojson(
    df,
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
    """Parameter to Set.

    df : Geodataframe
    color: geometry color (Any color / Random)
    tooltip: Tooltip (default: all columns)
    zoom: zoom level
    opacity: Opacity
    """
    gpd_copy = df.copy()
    if isinstance(color, list):
        gpd_copy["color"] = color
    elif color.lower() == "random":
        gpd_copy["color"] = _random_color_hex(len(df))
    else:
        gpd_copy["color"] = [color] * len(gpd_copy)

    geo_json = gpd_copy.__geo_interface__

    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    folium.GeoJson(
        geo_json,
        tooltip=folium.GeoJsonTooltip(fields=_get_tooltip(tooltip, gpd_copy)),
        style_function=lambda x: {"color": x["properties"]["color"], **style},
        name=name,
    ).add_to(m)
    return m


def chloropeth(
    df,
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

    gpd_copy = df.copy()
    colormap = _get_color_map(color, legend, gpd_copy, color_by)
    if not index_col:
        object_col = "unique_index"
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


class MarkerWithProps(Marker):
    """Custom markerclusters."""

    _template = Template(
        u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.marker(
            [{{this.location[0]}}, {{this.location[1]}}],
            {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }}
                {%- endif %}
                }
            )
            .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    def __init__(
        self, location, popup=None, tooltip=None, icon=None, draggable=False, props=None
    ):
        """Custom marker fucntion for folium markercluster."""
        super(MarkerWithProps, self).__init__(
            location=location,
            popup=popup,
            tooltip=tooltip,
            icon=icon,
            draggable=draggable,
        )
        self.props = json.loads(json.dumps(props))


average_function = """
    function(cluster) {
        var markers = cluster.getAllChildMarkers();
        var sum = 0;
        for (var i = 0; i < markers.length; i++) {
            sum += markers[i].options.props.population;
        }
        var avg = Math.floor(sum/cluster.getChildCount());
        return L.divIcon({
             html: '<b>' + avg + '</b>',
             className: 'marker-cluster marker-cluster-small',
             iconSize: new L.Point(30, 30)
        });
    }
"""


sum_function = """
    function(cluster) {
        var markers = cluster.getAllChildMarkers();
        var sum = 0;
        for (var i = 0; i < markers.length; i++) {
            sum += markers[i].options.props.population;
        }
        var avg = Math.floor(sum);
        return L.divIcon({
             html: '<b>' + avg + '</b>',
             className: 'marker-cluster marker-cluster-small',
             iconSize: new L.Point(30, 30)
        });
    }
"""


def markercluster(
    df,
    weight=None,
    metric=None,
    name="layer",
    width=950,
    height=550,
    location=None,
    zoom=7,
    tiles="OpenStreetMap",
    attr=None,
):

    gpd_copy = df.copy()

    col = gpd_copy._geometry_column_name
    lon = [lon.x for lon in gpd_copy[col]]
    lat = [lat.y for lat in gpd_copy[col]]
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    if weight is None:
        marker_cluster = MarkerCluster().add_to(m)
        for i in range(0, len(gpd_copy)):
            folium.Marker([lat[i], lon[i]]).add_to(marker_cluster)
    else:
        latlong_list = [list(latlong) for latlong in list(zip(lat, lon))]
        metric_list = list(gpd_copy[weight])
        value_weight_pair = tuple(
            [
                {"location": l, "metric": met}
                for l, met in zip(latlong_list, metric_list)
            ]
        )
        if metric is None or metric == "average":
            marker_cluster = MarkerCluster(icon_create_function=average_function)
        elif metric == "sum":
            marker_cluster = MarkerCluster(icon_create_function=sum_function)
        else:
            raise Exception("Input a valid metric")

        for marker_item in value_weight_pair:
            marker = MarkerWithProps(
                location=marker_item["location"],
                props={"population": marker_item["metric"]},
            )
            marker.add_to(marker_cluster)
        marker_cluster.add_to(m)
    return m


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
        gpd_copy, width, height, location, tiles=tiles,
        attr=attr, zoom_start=zoom
    )

    HeatMap(data, **style).add_to(m)
    return m
