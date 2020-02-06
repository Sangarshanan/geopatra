"""Combine plots and expose them with geopandas."""


import geopandas as gpd
from .folium import geojson, chloropeth, markercluster, heatmap


@gpd.tools.util.pd.api.extensions.register_dataframe_accessor("folium")
class InteraciveMap:
    def __init__(self, geopandas_obj):
        self._gdf = geopandas_obj

    def plot(self, **kwargs):
        gdf = self._gdf
        m = geojson(gdf, **kwargs)
        return m

    def chloropeth(self, **kwargs):
        gdf = self._gdf
        m = chloropeth(gdf, **kwargs)
        return m

    def markercluster(self, **kwargs):
        gdf = self._gdf
        m = markercluster(gdf, **kwargs)
        return m

    def heatmap(self, **kwargs):
        gdf = self._gdf
        m = heatmap(gdf, **kwargs)
        return m
