"""Combine plots and expose them with geopandas."""


import geopandas
from geopatra.folium import FoliumMap
from geopatra import kepler


@geopandas.tools.util.pd.api.extensions.register_dataframe_accessor("folium")
class InteractiveMapFolium:
    """Extends geopandas to enable easy interactive plotting with folium.

    Refer folium/ to call the below functions directly or to customize them
    """

    def __init__(self, geopandas_obj):
        """Init InteractiveMap with geodataframe."""
        self._gdf = geopandas_obj

    def plot(self, kind=None, **kwargs):
        """Plot geodataframe wih folium."""
        return FoliumMap(kind)(self._gdf, **kwargs)


@geopandas.tools.util.pd.api.extensions.register_dataframe_accessor("kepler")
class InteractiveMapKepler:
    """Extends geopandas to enable easy interactive plotting with kepler.

    Refer kepler/ to call the below functions directly or to customize them
    """

    def __init__(self, geopandas_obj):
        """Init InteractiveMap with geodataframe."""
        self._gdf = geopandas_obj

    def plot(self, **kwargs):
        """Plot geodataframe as a geojson."""
        m = kepler.geojson(self._gdf, **kwargs)
        return m
