# start with python image
FROM python:3.10-slim

# work directory
WORKDIR /app

# use requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy full project
COPY . .
RUN python manage.py migrate

EXPOSE 8000

# commands to start app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "first_project.wsgi:application"]
