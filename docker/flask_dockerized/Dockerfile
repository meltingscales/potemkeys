FROM python:3

MAINTAINER Henry Post "resplendent.falconeer@gmail.com"

#RUN apt-get update -y && \
#    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" "run", "--host", "0.0.0.0"]

