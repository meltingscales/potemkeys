# How do I run this?

## Install Python 3.6

Go to Python's website and install Python 3.6.

## Install dependencies

Run `pip install pipenv` to install a dependency manager called "pipenv".

Then, run `pipenv install` to install dependencies described in
`Pipfile`.

Then, you must enter the pipenv environment by running `pipenv shell` before you run any commands. This is done as 
it separates your system's python packages from this project's.

## Make and apply migrations

You only need these steps again whenever you change `models.py`.

### Make migrations

You can do this by running `python manage.py makemigrations orm_example`.

### Apply migrations

Apply the migrations by running `python manage.py migrate`.

## Run it 

Run `python manage.py runserver`.