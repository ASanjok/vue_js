## to start app in vs code

## move to dir django
cd django

## activate virtual environment
\env\Scripts\activate


## move to dir first_project
cd .\first_project\


## run project
python .\manage.py runserver

<!-- ------------------------------------ -->

## to create docker image

## create a requirements file
pip freeze > requirements.txt 

## build a docker image
## should be opened docker desktop
## next command must be entered in terminal with the same priveleges (admin, notAdmin)
docker build -t <your_image_name> .