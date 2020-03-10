"""Combine plots and expose them with geopandas."""


import geopandas
from geopatra import folium


@geopandas.tools.util.pd.api.extensions.register_dataframe_accessor("folium")
class InteractiveMap:
    """Extends geopandas to enable easy interactive plotting with folium.

    Refer folium/ to call the below functions directly or to customize them
    """

    def __init__(self, geopandas_obj):
        """Init InteractiveMap with geodataframe."""
        self._gdf = geopandas_obj

    def plot(self, **kwargs):
        """Plot geodataframe as a geojson."""
        m = folium.geojson(self._gdf, **kwargs)
        return m

    def circle(self, **kwargs):
        """Plot geodataframe as a geojson."""
        m = folium.circle(self._gdf, **kwargs)
        return m

    def chloropeth(self, **kwargs):
        """Plot geodataframe as a chloropeth."""
        m = folium.chloropeth(self._gdf, **kwargs)
        return m

    def markercluster(self, **kwargs):
        """Plot geodataframe as a markercluster."""
        m = folium.markercluster(self._gdf, **kwargs)
        return m

    def heatmap(self, **kwargs):
        """Plot geodataframe as a heatmap."""
        m = folium.heatmap(self._gdf, **kwargs)
        return m
