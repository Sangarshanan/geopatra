"""test geopatra with folium."""
import random
from geopatra import folium
import geopandas


class TestFolium:
    """Test class for the Folium library."""

    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    cities = geopandas.read_file(geopandas.datasets.get_path("naturalearth_cities"))
    cities["value"] = [int(random.randint(10, 1000)) for i in range(len(cities))]

    def test_geojson_plots(self):
        """Test folium plot."""
        geojson_map = folium.geojson(self.cities, zoom=5)
        assert geojson_map.options == {
            "zoom": 5,
            "zoomControl": True,
            "preferCanvas": False,
        }

    def test_circle_plots(self):
        """Test folium plot."""
        circle_map = folium.circle(self.cities, zoom=5)
        assert circle_map.options == {
            "zoom": 5,
            "zoomControl": True,
            "preferCanvas": False,
        }

    def test_choropleth_plots(self):
        """Test choropleth plot."""
        choropleth_map = folium.choropleth(
            self.world, location=[0, 0], color_by="pop_est", index_col="name"
        )

        assert choropleth_map.location == [0.0, 0.0]

        # without index
        choropleth_map = folium.choropleth(
            self.world, location=[0, 0], color_by="pop_est"
        )

        assert choropleth_map.location == [0.0, 0.0]

    def test_markercluster_plots(self):
        """Test markercluster plot."""
        markercluster_map = folium.markercluster(self.cities, location=[10, 20])
        assert markercluster_map.location == [10.0, 20.0]

    def test_heatmap_plots(self):
        """Test heatmap plot."""
        heatmap_map = folium.heatmap(self.cities, zoom=10)
        assert heatmap_map.options == {
            "zoom": 10,
            "zoomControl": True,
            "preferCanvas": False,
        }
