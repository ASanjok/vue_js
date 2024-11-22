# start with python image
FROM python:3.11-slim

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
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
