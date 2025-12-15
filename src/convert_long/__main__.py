"""Command line management."""

import argparse
from pathlib import Path
import sys

import geopandas as gpd

from convert_long import convert360


def main() -> None:
    "Parse command line arguments and execute."""

    parser = argparse.ArgumentParser(
            prog="Convert Longitude Range",
            description="Convert polygons in input file from longitude range [-180, 180] to [0, 360]; write result to output path.",
            )
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"ERROR: file '{args.input}' does not exist", file=sys.stderr)
        return
    else:
        gdf = gpd.read_file(Path(args.input))

    gdf360 = convert360(gdf)
    gdf360.to_file(args.output)
    print(f"Output polygons on range [0, 360] to file: '{args.output}'")


if __name__ == "__main__":
    main()
