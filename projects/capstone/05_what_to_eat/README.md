# Welcome to What To Eat Backend

This app works as a meal planner for users. It gives users suggestions based on their previous favorite take-out food items from various restaurants. It saves users time and energy to plan their meals. Especially when the restaurants are not fully opened with their sitting down area during this particular situation, you will spend lots of time on eating at home. What to eat app will plan your meals with the food you used to love. Using What to eat, your favorite food is just one button away. In the current version, users will be able to view the recommended dishes. Ordering feature will be available in the future versions.

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

### Running the server from local host
From within the `05_what_to_eat` directory (one level above `backend` directory) first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
DATABASE_URL='postgresql://localhost:5432/dish' PGGSSENCMODE=disable FLASK_APP=backend/src/app.py FLASK_ENV=development flask run
```

or you can export the environment first:
```bash
export DATABASE_URL='postgresql://localhost:5432/dish' 
export PGGSSENCMODE=disable 
export FLASK_APP=backend/src/app.py 
export FLASK_ENV=development 
flask run
```

### Running the server from Heroku
The app is deployed on Heroku. You can visit the app via: 

https://what-to-eat-by-rg.herokuapp.com/. 

Please note that the frontend code is not available yet. In order to test the APIs, please use Postman or curl methods with proper authentication information. For Postman, authentication token has been included in What_to_eat_heroku_deployment.postman_collection.json. Feel free to download this file and import in Postman before testing APIs.

### Retrieve tokens via Auth0
Auth0 link:
dev-auth2.auth0.com/authorize?audience=Dishes&response_type=token&client_id=eCc4Btc6EONcULa1scEWiIB32x3PZxBd&redirect_uri=https://127.0.0.1:8080/login

Admin login: cumulus166@gmail.com / password: Coffee123@@

User login: cumulus189@gmail.com / password: Coffee123@@

### Test.py
```bash
$ cd $PROJECT_PATH/backend
$ ls
$ __init__.py   src
$ python3 -m src.test
```
## API endpoints
### GET 'categories'
Returns a list of categories:
{
    "categories": [
        {
            "category": "Mexican",
            "id": 1
        },
        {
            "category": "Mexican",
            "id": 2
        },
        {
            "category": "Mexican",
            "id": 3
        }
    ],
    "success": true
}