# Convert longitude range

This Python package uses [GeoPandas][gpd] to convert polygons from longitude range [-180, 180] to range [0, 360].
The software is intended solely for visualization purposes;
namely, to create maps centred on the Pacific Ocean rather than Greenwich and the Atlantic.

In particular, users should note the following:

1. The conversion tool does not preserve a unique meridian;
values of ``0`` and ``360`` in the output polygons refer to the same longitude.
1. Polygons that span the antimeridian (180 degrees) are not merged into a single polygon.
For example, if the tool is applied to a polygon representing Antarctica, it will output two polygons, split at longitude 180 degrees.

# Installation

Clone this repository, change into the directory, and install the Python package with pip:

```
git clone https://github.com/elijahgreenstein/convert_longitude_range.git
cd convert_longitude_range
pip install .
```

# Usage

In this example, `data/world.shp` is a path to a Shapefile containing data for world continents:

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from convert_long import convert360
data = "data/world.shp"
gdf = gpd.read_file(data)
gdf360 = convert360(gdf)
gdf360.plot()
plt.show()
```

# Command line tool

This package also provides a command line tool, `convert_long360`, to load data from an input file, convert polygons to the [0, 360] range, and write the results to an output file.

```
convert_long360 data/world.shp data/world360.shp
```

Note that the output file path will be passed to [`geopandas.GeoDataFrame.to_file`][gpd_to_file], which will attempt to infer the output data format from the file extension.

[gpd]: https://geopandas.org/en/stable/index.html
[gpd_to_file]: https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html
