# Welcome to What To Eat Backend

This app works as a meal planner for users. It gives users suggestions based on their previous favorite take-out food items from various restaurants. It saves users time and energy to plan their meals. Especially when the restaurants are not fully opened with their sitting down area during this particular situation, you will spend lots of time on eating at home. What to eat app will plan your meals with the food you used to love. Using What to eat, your favorite food is just one button away.

## Virtual environment is recommended.

Instructions for setting up virtual environment can be found at: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments

## PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages which are selected within the `requirements.txt` file.

## Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
PGGSSENCMODE=disable FLASK_APP=./src/app.py FLASK_DEBUG=TRUE flask run
```

## Todos

### Setup Auth0

### Implement server

./src/auth/auth.py
./src/app.py