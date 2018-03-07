import shapefile, zipfile, json, os
from topojson import topojson
import pandas as pd
from io import StringIO, BytesIO
from os import path


class ShapefileToTopojson(object):
  def __init__(self, in_files: str, out_file: [str, None]) -> None:

    self.in_files = in_files if isinstance(in_files, list) else [in_files]
    self.out_file = out_file

    self.convert()
    return None

  def convert(self) -> None:

    buffer = []
    properties = []

    for in_file in self.in_files:

      in_zip = path.split(in_file)[1]

      in_name, ext = in_zip.split('.')
      in_name = in_name + '.{}'

      if ext != 'zip':
        raise ValueError('Expected `in_file` to be a zip file.')

      zipshape = zipfile.ZipFile(open(in_file, 'rb'))

      # read the shapefile
      reader = shapefile.Reader(
        shp=BytesIO(zipshape.read(in_name.format('shp'))),
        shx=BytesIO(zipshape.read(in_name.format('shx'))),
        dbf=BytesIO(zipshape.read(in_name.format('dbf')))
      )
      fields = reader.fields[1:]
      field_names = [field[0] for field in fields]
      for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        properties.append(atr)
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    # Write everything to file.
    if self.out_file is None:
      out_dir, out_zip = path.split(in_files[0])
      out_name, ext = out_zip.split('.')
      out_name = out_name + '.{}'
      out_file = path.join(in_dir, out_name.format('json'))
    else:
      out_file = self.out_file
      out_dir, out_zip = path.split(out_file)

      out_name, ext = out_zip.split('.')
      out_name = out_name + '.{}'

      if ext != 'json':
        raise ValueError(
          'Expected `out_file` to be a `json` file. Instead got: {}'.
          format(ext)
        )

    # write the GeoJSON file
    temp_file = path.join(out_dir, 'temp_' + out_name.format('json'))
    with open(temp_file, 'w') as geojson:
      json.dump({"type": "FeatureCollection", "features": buffer}, geojson)

    # Write the topojson file
    topojson(temp_file, out_file)

    # Delete GeoJson File
    os.remove(temp_file)

    # Make the properties into a pandas dataframe
    self.properties = pd.DataFrame(properties)
    return None


if __name__ == '__main__':
  inf = '../data/raw/puma_shapefiles/cb_2016_01_puma10_500k.zip'
  outf = '../data/int/shapefiles/cb_2016_01_puma10_500k.json'

  stj = ShapefileToTopojson(inf, outf)
