#  Set python 3.7  Linux environment
FROM python:3.7

# set python environment variable
ENV PYTHONUNBUFFERED 1

# create code folder and set as a working dir
RUN mkdir /app
WORKDIR /app
COPY . /app/

# update pip
RUN pip install pip -U

# install dependency
RUN pip install -r requirements.txt
# RUN mkdir bus_stops/staticfiles
# RUN python manage.py collectstatic --noinput
#start the django server and the PORT variable will be given by Heroku
CMD python manage.py runserver 0.0.0.0:$PORT

