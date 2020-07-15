from geopatra import folium


class FoliumMap(object):
    """docstring for FoliumMap."""

    def __init__(self, kind):
        super(FoliumMap, self).__init__()
        self.kind = kind

    def __call__(self, gdf, **kwargs):
        kind = self.kind
        if (kind == "default") or (kind is None):
            m = folium.geojson(gdf, **kwargs)
        elif kind == "circle":
            m = folium.circle(gdf, **kwargs)
        elif kind == "markercluster":
            m = folium.markercluster(gdf, **kwargs)
        elif kind == "heatmap":
            m = folium.heatmap(gdf, **kwargs)
        else:
            raise Exception("Kind must be circle, heatmap or markercluster")
        return m
