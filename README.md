# start docker compose in terminal


in django/project/project/settings.py comment lines

```sh
GDAL_LIBRARY_PATH = r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\gdal303.dll"
os.environ["GDAL_LIBRARY_PATH"] = GDAL_LIBRARY_PATH

GEOS_LIBRARY_PATH = r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\geos_c.dll"
os.environ["GEOS_LIBRARY_PATH"] = GEOS_LIBRARY_PATH

.
.
.

'HOST': 'localhost',
```
and uncomment
```sh
'HOST': 'host.docker.internal',
```

create a requirements file

```sh
pip freeze > requirements.txt 
```

in django/project/dockerfile comment line about GDAL

something like:
```sh
GDAL @ file:///C:/Users/aleksandrs.sloka/Desktop/vs_codes/vue_js/django/GDAL-3.3.1-cp39-cp39-win_amd64.whl
```
in root directory __*terminal with the same rights as docker engine*__ <br>
build and start docker containers

```sh
docker-compose build
docker-compose up
```

