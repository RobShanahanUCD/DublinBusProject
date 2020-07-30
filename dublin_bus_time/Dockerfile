#  Set python 3.7  Linux environment
FROM python:3.7

# set python environment variable
ENV PYTHONUNBUFFERED 1

# create code folder and set as a working dir
RUN mkdir /code
WORKDIR /code
# update pip
RUN pip install pip -U
RUN pip install mysqlclient
RUN pip install pymysql
# copy requirements.txt to code dir
ADD requirements.txt /code/
# install dependency
RUN pip install mysqlclient
RUN pip install -r requirements.txt
# duplicate current to code
ADD . /code/

