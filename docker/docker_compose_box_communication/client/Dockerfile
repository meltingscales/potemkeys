FROM python:3

LABEL maintainer="Henry Post, resplendent.falconeer@gmail.com, http://henryfbp.me/"

RUN apt-get update

RUN apt-get install iputils-ping curl

ENTRYPOINT [ "curl" ]
CMD [ "http://web:8000/" ]