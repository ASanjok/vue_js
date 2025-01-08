# install project
 create virtual environment
```sh
cd django

python -m venv ./env
```
 install requirement dpendencies

```sh
cd first_project  

pip install -r requirements.txt
```

<!-- ------------------------------------ -->

# to start app in terminal

install Python 3.9 (if not already installed) [install Python 3.9](https://www.python.org/downloads/release/python-3910/).

# check how to install GDAL at new project (is it installed ) 

in django/project/project/settings.py __*uncomment*__ lines

```sh
GDAL_LIBRARY_PATH = r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\gdal303.dll"
os.environ["GDAL_LIBRARY_PATH"] = GDAL_LIBRARY_PATH

GEOS_LIBRARY_PATH = r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\geos_c.dll"
os.environ["GEOS_LIBRARY_PATH"] = GEOS_LIBRARY_PATH
```
and
```sh
'HOST': 'localhost',
```
and comment
```sh
'HOST': 'host.docker.internal',
```

move to dir django
```sh
cd django
```

 activate virtual environment
```sh
\env\Scripts\activate
```

 move to dir "project"
```sh
cd .\project\
```

 run project
```sh
python .\manage.py runserver
```
<!-- ------------------------------------ -->

# to create docker image

 create a requirements file
```sh
pip freeze > requirements.txt 
```
 build a docker image
should be opened docker desktop<br />
next command must be entered in terminal with the same priveleges (admin, notAdmin)
```sh
docker build -t <your_image_name> .
```

# login password /admin/
login - admin   
password - 1234