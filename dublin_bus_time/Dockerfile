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

# copy requirements.txt to code dir
ADD requirements.txt /app/
# install dependency
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:$PORT

