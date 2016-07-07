import glob, os
from geoserver.catalog import Catalog
os.chdir("sld")
cat = Catalog("http://localhost:48080/minresource-minesatlas-gws/rest")
for file in glob.glob("*.sld"):

    with open(file) as f:
        sld_name = os.path.splitext(file)[0]
        cat.create_style(sld_name, f.read(), overwrite=True)
        
    