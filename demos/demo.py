import os

from ShapefileToTopojson import ShapefileToTopojson

# One Shapefile

inf = 'demos/data/shapefiles/cb_2016_01_puma10_500k.zip'
outf = 'demos/data/topojson/one_file_demo_AL.json'

stj = ShapefileToTopojson(inf, outf)

# See information about the features:
print(stj.properties)

# Multiple Shapefiles => Merged output

input_template = 'demos/data/shapefiles/cb_2016_{:02d}_puma10_500k.zip'
inf = [
  input_template.format(ii)
  for ii in range(79)
  if os.path.exists(input_template.format(ii))
]
outf = 'demos/data/topojson/merged_file_demo.json'

stj = ShapefileToTopojson(inf, outf)
