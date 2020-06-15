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
From within the working directory (for example, mine is `05_what_to_eat` directory, which is one level above `backend` directory) first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
$ DATABASE_URL='postgresql://localhost:5432/dish' PGGSSENCMODE=disable FLASK_APP=backend/src/app.py FLASK_ENV=development flask run
```

or you can export the environment first:
```bash
$ export DATABASE_URL='postgresql://localhost:5432/dish' 
$ export PGGSSENCMODE=disable 
$ export FLASK_APP=backend/src/app.py 
$ export FLASK_ENV=development 
$ flask run
```

or you can run `setup.sh` from the working directory. 
```bash
$ chmod +x setup.sh // only need to run this command before using this script for the first time.
$ ./setup.sh // It creates datebase dish first and then runs the server.
```

### Running the server from Heroku
The app is deployed on Heroku. You can visit the app via: 

https://what-to-eat-by-rg.herokuapp.com/. 

Please note that the frontend code is not available yet. In order to test the APIs, please use Postman or curl methods with proper authentication information. For Postman, authentication token has been included in [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat.postman_collection.json). Feel free to download this file and import in Postman before testing APIs.

### Retrieve tokens via Auth0
Auth0 link:
https://dev-auth2.auth0.com/authorize?audience=Dishes&response_type=token&client_id=eCc4Btc6EONcULa1scEWiIB32x3PZxBd&redirect_uri=https://127.0.0.1:8080/login

Admin login: cumulus166@gmail.com / password: Coffee123@@

User login: cumulus189@gmail.com / password: Coffee123@@

## Data modeling
**model.py** includes database schema and helper functions such as insert, update, delete and format functions. There are three tables created in the database: **Category**, **Restaurant** and **Dish**. Only Admin users can create, update and delete entries from the tables. Regular users can only view the entries in the three tables. Users can also search for dishes and get recommended new dishes. 

### Category

The category object describes the type of a dish. The API allows you to get, post, delete and update categories. You can retrieve a single category or a list of categories from the existing category collection. Only users with admin permissions can create, delete and update category object. Regular users without admin permissions can browse category information.

### Restuarant

The restaurant object describes a restaurant with attributes as name, city, state, address, image link and website infomration . The API allows you to get, post, delete and update restaurants. You can retrieve a single restaurant or a list of restaurants from the existing restaurant collection. Only users with admin permissions can create, delete and update restaurant object. Regular users without admin permissions can browse restaurant information.

### Dish

The category object describes a dish with attributes as name, restaurant_id, category_id, price, rating and image link . The API allows you to get, post, delete and update dishes. You can retrieve a single dish or a list of dishes from the existing dish collection. Only users with admin permissions can create, delete and update dish object. Regular users without admin permissions can browse dish information. These users can also search for dishes and get recommended new dishes.

## API endpoints

### Category

#### GET '/categories'
- Fetches a list of categories from the existing category collection.
- Return a list of objects with id and category key:value pairs.
- No arguments required.

##### Exmaple request:
`GET /categories`

##### Exmaple response:

```javascript
{
    "categories": [
        {
            "category": "Mexican",
            "id": 1
        },
        {
            "category": "American",
            "id": 2
        }
    ],
    "success": true
}
```

#### GET '/categories/{category_id}'
- Retrieve a specified category by category_id from the category collection.
- Requested arguments: **category_id**
- Return an object with matched catory and a successful message.

##### Exmaple request:
`GET /categories/1`

##### Exmaple response:

```javascript
{
    "category": {
        "category": "Mexican",
        "id": 1
    },
    "success": true
}
```

#### POST '/categories'
- Requires **Admin** authentication.
- Create a new category in the existing category collection.
- Return an object with an object of newly added catogry and a successful message.
- No arguments required.

##### Exmaple request:
`POST /categories`

```javascript
{
	"category": "Chinese"
}
```

##### Exmaple response:
```javascript
{
    "new_category": {
        "category": "Chinese",
        "id": 3
    },
    "success": true
}
```

#### DELETE '/categories/{category_id}'
- Requires **Admin** authentication.
- Delete a specified category based on the category_id.
- Request arguments: **category_id**
- Returns: An object with the deleted category id, the existing category collection and a successful message.

##### Exmaple request:
`DELETE /categories/3`

##### Exmaple response:

```javascript
{
    "categories": [
        {
            "category": "Mexican",
            "id": 1
        },
        {
            "category": "American",
            "id": 2
        }
    ],
    "delete_id": 3,
    "success": true
}
```

#### PATCH '/categories/{category_id}'
- Requires **Admin** authentication.
- Update a specified question based on the category_id
- Request arguments: **category_id**
- Body: Category to update to.
- Returns: A category object with the updated category information and a successful message.

##### Exmaple request:
`PATCH /categories/1`

```javascript
{
	"category": "Chinese"
}
```

##### Exmaple response:
```javascript
{
    "success": true,
    "updated category": {
        "category": "Chinese",
        "id": 1
    }
}
```

### Restuarant

#### GET '/restaurants'
- Fetches a list of restaurants from the existing restaurant collection.
- Return a list of restaurant objects with id, name, city, state, address, website and r_image_link key:value pairs.
- No arguments required.

##### Exmaple request:
`GET /restaurants`

##### Exmaple response:

```javascript
{
    "restaurants": [
        {
            "address": "Sandwich Monkey address",
            "city": "San Carlos",
            "id": 1,
            "name": "Sandwich Monkey",
            "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
            "state": "CA",
            "website": "www.sandwichmonkey.com"
        }
    ],
    "success": true
}
```
#### GET '/restaurants/{restaurant_id}'
- Retrieve a specified restaurant by restaurant_id from the restaurant collection.
- Requested arguments: **restaurant_id**
- Return a matched restaurant object and a successful message.

##### Exmaple request:
`GET /restaurants/1`

##### Exmaple response:

```javascript
{
    "restaurant_by_id": {
        "address": "Sandwich Monkey address",
        "city": "San Carlos",
        "id": 1,
        "name": "Sandwich Monkey",
        "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
        "state": "CA",
        "website": "www.sandwichmonkey.com"
    },
    "success": true
}
```

#### POST '/restaurants'
- Requires **Admin** authentication.
- Create a new restaurant in the existing restaurant collection.
- Return an object with an object of newly added restaurant and a successful message.
- No arguments required.

##### Exmaple request:
`POST /restaurants`

```javascript
{
  "city": "San Carlos",
  "name": "Hot Dog House",
  "address": "Hot Dog House address",
  "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
  "state": "CA",
  "website": "www.hotdoghause.com"
}
```

##### Exmaple response:
```javascript
{
    "new_restaurant": {
        "address": "Hot Dog House address",
        "city": "San Carlos",
        "id": 2,
        "name": "Hot Dog House",
        "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
        "state": "CA",
        "website": "www.hotdoghause.com"
    },
    "success": true
}
```

#### DELETE '/restaurants/{restaurant_id}'
- Requires **Admin** authentication.
- Delete a specified restaurant based on the restaurant_id.
- Request arguments: **restaurant_id**
- Returns: An object with the deleted restaurant id, the existing restaurant collection after deletion and a successful message.

##### Exmaple request:
`DELETE /restaurants/2`

##### Exmaple response:

```javascript
{
    "deleted_restaurant_id": 2,
    "restaurants_after_deletion": [
        {
            "address": "Sandwich Monkey address",
            "city": "San Carlos",
            "id": 1,
            "name": "Sandwich Monkey",
            "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
            "state": "CA",
            "website": "www.sandwichmonkey.com"
        }
    ],
    "success": true
}
```

#### PATCH '/restaurants/{restaurant_id}'
- Requires **Admin** authentication.
- Update a specified restaurant based on the restaurant_id
- Request arguments: **restaurant_id**
- Body: Restaurant's attributes to update to.
- Returns: A restaurant object with the updated attributes and a successful message.

##### Exmaple request:
`PATCH /restaurants/1`

```javascript
{
  "city": "Foster City"
}
```

##### Exmaple response:
```javascript
{
    "success": true,
    "updated_restaurant": {
        "address": "Sandwich Monkey address",
        "city": "Foster City",
        "id": 1,
        "name": "Sandwich Monkey",
        "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
        "state": "CA",
        "website": "www.sandwichmonkey.com"
    }
}
```

### Dish

#### GET '/dishes'
- Fetches a list of dishes from the existing dish collection.
- Return a list of dish objects with id, name, restaurant_id, category_id, price, rating, image_link key:value pairs.
- No arguments required.

##### Exmaple request:
`GET /dishes`

##### Exmaple response:

```javascript
{
    "dishes": [
        {
            "category_id": 2,
            "id": 1,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "BBQ Salad",
            "price": 10,
            "rating": 4,
            "restaurant_id": 1
        },
        {
            "category_id": 2,
            "id": 2,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "Cob Salad",
            "price": 10,
            "rating": 3,
            "restaurant_id": 1
        }
    ],
    "success": true
}
```

#### GET '/dishes/{dish_id}'
- Retrieve a specified dish by dish_id from the dish collection.
- Requested arguments: **dish_id**
- Return an object with matched dish and a successful message.

##### Exmaple request:
`GET /dishes/1`

##### Exmaple response:

```javascript
{
    "dish": {
        "category": "American",
        "category_id": 2,
        "id": 1,
        "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
        "name": "BBQ Salad",
        "price": 10,
        "rating": 4,
        "restaurant_id": 1,
        "restaurant_name": "Sandwich Monkey"
    },
    "success": true
}
```

#### POST '/dishes'
- Requires **Admin** authentication.
- Create a new dish in the existing dish collection.
- Return an object with an object of newly added dish and a successful message.
- No arguments required.

##### Exmaple request:
`POST /dishes`

```javascript
{
	"name": "BBQ Hot Dog",
	"restaurant_id": 2,
	"category_id": 2,
	"rating": 3,
	"price": 6.00,
	"image_link": null
}
```

##### Exmaple response:
```javascript
{
    "new_dish": {
        "category_id": 2,
        "id": 3,
        "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
        "name": "BBQ Hot Dog",
        "price": 6,
        "rating": 3,
        "restaurant_id": 2
    },
    "success": true
}
```

#### DELETE '/dishes/{dish_id}'
- Requires **Admin** authentication.
- Delete a specified dish based on the dish_id.
- Request arguments: **dish_id**
- Returns: An object with the deleted dish id and a successful message.

##### Exmaple request:
`DELETE /dishes/3`

##### Exmaple response:

```javascript
{
    "deleted_dish_id": 3,
    "success": true
}
```

#### PATCH '/dishes/{dish_id}'
- Requires **Admin** authentication.
- Update a specified dish based on the dish_id
- Request arguments: **dish_id**
- Body: Dish object's attributes to update to.
- Returns: A dish object with the updated dish information and a successful message.

##### Exmaple request:
`PATCH /dishes/1`

```javascript
{
	"rating": 5
}
```

##### Exmaple response:
```javascript
{
    "dish": {
        "category": "American",
        "category_id": 2,
        "id": 1,
        "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
        "name": "BBQ Salad",
        "price": 10,
        "rating": 5,
        "restaurant_id": 1,
        "restaurant_name": "Sandwich Monkey"
    },
    "success": true
}
```

#### GET '/categories/{category_id}/dishes'
- Retrieve a list of dishes from the same category by category_id
- Request arguments: **category_id**
- Returns: A list of dishes grouped by a given category_id and a successful message.

##### Exmaple request:
`GET /categories/2/dishes`

##### Exmaple response:
```javascript
{
    "dishes_by_categories": [
        {
            "category": "American",
            "category_id": 2,
            "id": 1,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "BBQ Salad",
            "price": 10,
            "rating": 3,
            "restaurant_id": 1,
            "restaurant_name": "Steak House"
        },
        {
            "category": "American",
            "category_id": 2,
            "id": 3,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "BBQ Hot Dog",
            "price": 6,
            "rating": 3,
            "restaurant_id": 2,
            "restaurant_name": "Hot Dog House"
        }
    ],
    "success": true
}
```

#### GET '/restaurants/{restaurant_id}/dishes'
- Retrieve a list of dishes from the same restaurant by restaurant_id
- Request arguments: **restaurant_id**
- Returns: A list of dishes grouped by a given restaurant_id and a successful message.

##### Exmaple request:
`GET /restaurants/1/dishes`

##### Exmaple response:
```javascript
{
    "dishes_by_restaurants": [
        {
            "category": "American",
            "category_id": 2,
            "id": 3,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "BBQ Salad",
            "price": 10,
            "rating": 3,
            "restaurant_id": 1,
            "restaurant_name": "Sandwich Monkey"
        },
        {
            "category": "American",
            "category_id": 2,
            "id": 8,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "Breakfast sandwich",
            "price": 6,
            "rating": 3,
            "restaurant_id": 1,
            "restaurant_name": "Sandwich Monkey"
        }
    ],
    "success": true
}
```

#### POST '/dishes/search'
- Search one or a group of dishes by a query string
- Return an object with matched dishes and a successful message.
- No arguments required.

##### Exmaple request:
`POST /dishes/search`

```javascript
{
   "search_term": "Sandwich"
}
```

##### Exmaple response:
```javascript
{
    "dishes": [
        {
            "category": "American",
            "category_id": 2,
            "id": 8,
            "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
            "name": "Breakfast sandwich",
            "price": 6,
            "rating": 3,
            "restaurant_id": 1,
            "restaurant_name": "Sandwich Monkey"
        }
    ],
    "success": true
}
```

#### POST '/dishes/try'
- Fetch a recommended dish with the category that is specified by users and is not from the previous dishes. If no category is specified, then return a dish that is not from the previous dishes and the rating is equal to or greater than 3. If a category is specified, then return a dish that is from the specified category but not from the previous dishes, and the rating is equal to or greater than 3.
- Return an object with the dish to try and a successful message.
- No arguments required.

##### Exmaple request:
`POST /dishes/try`

```javascript
{
	"previous_dishes": [4],
	"new_category":2
}
```

##### Exmaple response:
```javascript
{
    "dish_to_try": {
        "category": "American",
        "category_id": 2,
        "id": 6,
        "image_link": "https://unsplash.com/photos/1Rm9GLHV0UA",
        "name": "BBQ Hot Dog",
        "price": 6,
        "rating": 3,
        "restaurant_id": 3,
        "restaurant_name": "Hot Dog House"
    },
    "success": true
}
```

## Testing
There are two ways to test the app. You can either use the test.py or Postman to run the test. 

#### Test.py
From within the working directory which is one level up from `backend` directory, run the following command.
```bash
$ createdb dish_test // setup test database
$ cd $PROJECT_PATH
$ python3 -m backend.src.test
```

#### Use Postman to run testing
Role related token has been added to the collection file [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat.postman_collection.json).
1. Launch Postman.
2. Import the above collection file to Postman.
3. Click the arrow next to the collection name and click Run to start the Collection Runner.
4. Check the test results.