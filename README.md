The main object, `ShapefileToTopojson`, converts (and merges) shapefiles to topojson format. It was created with U.S. Census Bureau Shapefiles in mind.

See `demos/demo.py` for an illustration of usage cases.

It is not a proper package and could be improved along a number of dimensions:

- Add inline documentation(!)
- Allow custom input of `shp`, `shx`, and `dbf` filenames.
- Deal with cases where the shapefile isn't archived or is archived in a non-`.zip` format.

Tested on Python 3 on ubuntu/linux.






