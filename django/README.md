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

move to dir django
```sh
cd django
```


 activate virtual environment
```sh
\env\Scripts\activate
```

 move to dir first_project
```sh
cd .\first_project\
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