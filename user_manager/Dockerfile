FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# create and assign the working directory
RUN mkdir /app
WORKDIR /app

# install dependency manager
RUN pip3 install pipenv

# install dependencies
COPY Pipfile* ./
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip3 install -r requirements.txt

# move all files in root directory to working directory
COPY . /app

# move into working directory
CMD cd ./app

# python server will be running on this port
EXPOSE 5000

# configures the container to run as an executable
ENTRYPOINT [ "python" ]

# start flask application
CMD [ "app.py" ]
