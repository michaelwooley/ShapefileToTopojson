import os

from ShapefileToTopojson import ShapefileToTopojson

# Data Source: https://www.census.gov/geo/maps-data/data/cbf/cbf_puma.html

# One Shapefile

inf = 'demos/data/shapefiles/cb_2016_01_puma10_500k.zip'
outf = 'demos/data/topojson/one_file_demo_AL.json'

stj = ShapefileToTopojson(inf, outf)

# See information about the features:
print(stj.properties)

# Multiple Shapefiles => Merged output

input_template = 'demos/data/shapefiles/cb_2016_{:02d}_puma10_500k.zip'

# Southeast
inf = [input_template.format(ii) for ii in [1, 5, 13, 12, 28, 37, 45, 47, 22]]
outf = 'demos/data/topojson/southeast_us_puma_2016.json'

stj = ShapefileToTopojson(inf, outf)

# Entire US
inf = [
  input_template.format(ii)
  for ii in range(79)
  if os.path.exists(input_template.format(ii))
]
outf = 'demos/data/topojson/us_puma_2016.json'

stj = ShapefileToTopojson(inf, outf)
