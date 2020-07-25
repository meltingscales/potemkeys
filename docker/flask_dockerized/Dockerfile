FROM python:3

MAINTAINER Henry Post "resplendent.falconeer@gmail.com"

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt 

COPY . /app
WORKDIR /app

EXPOSE 5001 

ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
