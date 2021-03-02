FROM ubuntu:20.04
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 5000 
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ]
