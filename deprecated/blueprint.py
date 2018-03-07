import shapefile, zipfile, json, os
from topojson import topojson
from io import StringIO, BytesIO
from os import path

name = 'cb_2016_01_puma10_500k.{}'
in_dir = '../data/raw/puma_shapefiles'
out_dir = '../data/int/shapefiles'

zipshape = zipfile.ZipFile(open(path.join(in_dir, name.format('zip')), 'rb'))

# read the shapefile
reader = shapefile.Reader(
  shp=BytesIO(zipshape.read(name.format('shp'))),
  shx=BytesIO(zipshape.read(name.format('shx'))),
  dbf=BytesIO(zipshape.read(name.format('dbf')))
)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
  atr = dict(zip(field_names, sr.record))
  geom = sr.shape.__geo_interface__
  buffer.append(dict(type="Feature", \
   geometry=geom, properties=atr))

# write the GeoJSON file
temp_file = path.join(out_dir, 'temp_' + name.format('json'))
out_file = path.join(out_dir, name.format('json'))
with open(temp_file, 'w') as geojson:
  json.dump({"type": "FeatureCollection", "features": buffer}, geojson)

topojson(temp_file, out_file)
os.remove(temp_file)
