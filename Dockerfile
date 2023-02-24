FROM alpine:3.14

ENV DEBIAN_FRONTEND noninteractive
# install python
RUN apk add py3-pip
# install flask environment 
RUN pip install Flask


ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /code
# creating a directory cache and changing permissions
RUN mkdir /.code && chmod 777 /.code


# copy the python file name
COPY fetchBackend.py /code/
# requirements for all docker environment should be here
COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir /.cache && chmod 777 /.cache
CMD tail -f /dev/null

