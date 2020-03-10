"""Folium markercluster Plot."""

import json
import folium
from folium import Marker
from jinja2 import Template
from folium.plugins import MarkerCluster

from .utils import _get_lat_lon, _folium_map, _get_tooltip


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
    gdf,
    weight=None,
    metric=None,
    name="layer",
    tooltip=None,
    width=950,
    height=550,
    location=None,
    zoom=7,
    tiles="OpenStreetMap",
    attr=None,
    kwargs={},
):
    """
    Plot a MarkerCluster map out of a geodataframe.

    Parameters
    ----------
    gdf : GeoDataframe
    weight : Custom markercluser, Column used to weight the metrics, optional
    metric : Custom markercluser, Metric for clustering, based on weight column
            available metrics: ['sum','average']
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
    gpd_copy = _get_lat_lon(gdf.copy())
    m = _folium_map(
        gpd_copy, width, height, location, tiles=tiles, attr=attr, zoom_start=zoom
    )
    if weight is None:
        marker_cluster = MarkerCluster(**kwargs).add_to(m)
        for index, row in gpd_copy.iterrows():
            tooltip_cols = _get_tooltip(tooltip, gpd_copy)
            tooltip_dict = {k: v for k, v in dict(row).items() if k in tooltip_cols}
            tooltip = "".join(
                [
                    "<p><b>{}</b> {}</p>".format(keyvalue[0], keyvalue[1])
                    for keyvalue in list(tooltip_dict.items())
                ]
            )
            folium.Marker(
                location=[row["latitude"], row["longitude"]], tooltip=tooltip
            ).add_to(marker_cluster)
    else:
        latlong_list = [
            list(latlong)
            for latlong in list(zip(gpd_copy["latitude"], gpd_copy["longitude"]))
        ]
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
