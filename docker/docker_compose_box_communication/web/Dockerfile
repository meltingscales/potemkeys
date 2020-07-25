FROM python:3

LABEL maintainer="Henry Post, resplendent.falconeer@gmail.com, http://henryfbp.me/"

# RUN pip install --upgrade pip

# RUN pip install flask

# testing build arguments
ARG TEST
RUN echo TEST argument is $TEST

ENTRYPOINT [ "python2" ] 
CMD [ "-m", "SimpleHTTPServer", "8000" ]