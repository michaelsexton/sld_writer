import glob, os
from geoserver.catalog import Catalog
os.chdir("sld")
cat = Catalog("http://localhost:28080/earthresource/rest")
for file in glob.glob("*.sld"):

    with open(file) as f:
        print file
        sld_name = os.path.splitext(file)[0]
        cat.create_style(sld_name, f.read(), overwrite=True)
        
    
