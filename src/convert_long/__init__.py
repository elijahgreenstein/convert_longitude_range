"""Convert polygons from longitude range [-180, 180] to [0, 360].

.. note::

   The data must be in a geographic coordinate reference system.

Example usage:

>>> import geopandas as gpd
>>> import matplotlib.pyplot as plt
>>> from convert_long import convert360
>>> data = "path/to/data/file.shp"
>>> gdf = gpd.read_file(data)
>>> gdf360 = convert360(gdf)
>>> gdf360.plot()
<Axes: >
>>> plt.show()
"""

from geopandas import GeoDataFrame
import pandas as pd
from shapely import MultiPolygon, Polygon


def convert360(gdf: GeoDataFrame) -> GeoDataFrame:
    """Split polygons; convert to :math:`[0, 360]` longitude range.

    This function first splits polygons on the prime meridian (:math:`0.0\\degree`).
    It then converts polygons west of the prime meridian (i.e. polygons with negative longitude on the range :math:`[-180, 180]`) to the range :math:`[0, 360]`.

    .. note::

       This function is intended solely for visualization purposes.
       Notably:

       #. This function does not preserve a unique meridian; values of ``0`` and ``360`` refer to the same longitude.
       #. Polygons that span the antimeridian (:math:`180.00\\degree`) are not merged into a single polygon.
    """
    west, east = split_polygons(gdf)
    west["geometry"] = west["geometry"].apply(converter)
    return pd.concat([west, east])


def split_polygons(gdf: GeoDataFrame) -> tuple[GeoDataFrame, GeoDataFrame]:
    """Split polygons along reference meridian, :math:`0\\degree`."""
    west = gdf.clip([-180, -90, 0, 90]).copy()
    east = gdf.clip([0, -90, 180, 90]).copy()
    return (west, east)


def convert_polygon(polygon: Polygon) -> Polygon:
    """Convert polygon to longitude range :math:`[0, 360]`.

    .. note::

       This function can only convert polygons that are entirely located in the *western* hemisphere;
       i.e. polygons with a maximum longitude of :math:`0\\degree`.
    """
    new_pts = []
    for pt in polygon.exterior.coords:
        new_pts.append((pt[0] + 360.0, pt[1]))
    return Polygon(new_pts)


def convert_multipolygon(multipolygon: MultiPolygon) -> MultiPolygon:
    """Convert multipolygon to longitude range :math:`[0, 360]`."""
    return MultiPolygon([convert_polygon(pg) for pg in multipolygon.geoms])


def converter(shape: Polygon | MultiPolygon) -> Polygon | MultiPolygon:
    """Pass shape to appropriate conversion function."""
    if isinstance(shape, Polygon):
        return convert_polygon(shape)
    if isinstance(shape, MultiPolygon):
        return convert_multipolygon(shape)
    raise ValueError(
        f"Can only convert Polygon or MultiPolygon shapes, not '{type(shape)}'."
    )
