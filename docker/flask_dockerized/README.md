<https://runnable.com/docker/python/dockerize-your-flask-application>

<https://www.geeksforgeeks.org/dockerize-your-flask-app/>

## Running locally

	python app.py

## Building the Docker image

	sudo docker build --tag flask-dockerized .

## Running the Docker image

	sudo docker run --name flask-dockerized -p 5001:5001 flask-dockerized