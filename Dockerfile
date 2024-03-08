FROM python:3.11.4-slim

COPY /server.py /usr/src/app/
WORKDIR /usr/src/app

RUN pip install fakeredis 

EXPOSE 6379
CMD [ "python", "server.py" ]