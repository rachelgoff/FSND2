# Welcome to the What To Eat Backend

This app works as a meal planner for users. It gives users suggestions based on their previous favorite take-out food items from various restaurants. It saves users' time and energy to plan their meals. Especially when the restaurants are not fully opened with their sitting down area during this particular situation, users will spend lots of time on eating at home. The What To Eat app will plan users' meals with the food they used to love. Using What To Eat, your favorite food is just one button away. In the current version, users will be able to view the recommended dishes. Ordering feature will be available in the future versions.

## Virtual environment

Virtual environment is highly recommended. Instructions for setting up virtual environment can be found at: [Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments).

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

## Working Directory
Go to the directory where you check out the [repository](https://github.com/rachelgoff/FSND2) which includes What To Eat backend code. The working directory is under `FSND2/projects/capstone/05_what_to_eat`.

## Running the server

### Running the server from localhost
Make sure you are working using your created virtual environment before you start running the server. Go to the working directory `FSND2/projects/capstone/05_what_to_eat`, then run the following command:

```bash
$ DATABASE_URL='postgresql://localhost:5432/dish' PGGSSENCMODE=disable FLASK_APP=backend/src/app.py FLASK_ENV=development flask run
```

or you can export the environment first:
```bash
$ createdb dish
$ export DATABASE_URL='postgresql://localhost:5432/dish' 
$ export PGGSSENCMODE=disable 
$ export FLASK_APP=backend/src/app.py 
$ export FLASK_ENV=development 
$ flask run
```

or you can run `setup.sh` from the working directory. 
```bash
$ chmod +x setup.sh
$ ./setup.sh
```

### Deployment on Heroku
The app's backend server is deployed on Heroku. You can visit and interact with the app's backend server via: 

https://what-to-eat-by-rg.herokuapp.com/. 

Please note that the frontend code is not available yet. In order to test the APIs, please use Postman with proper authentication information. For Postman, the authentication tokens have been included in [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat_heroku_deployment.postman_collection.json). Feel free to download this collection.json file and import it in Postman before testing APIs.

## Data modeling
**model.py** includes database schema and helper functions such as insert, update, delete and format functions. There are three tables created in the database: **categories**, **restaurants** and **dishes**. Only Admin users can create, update and delete entries from the tables. Regular users can only view the entries in the three tables. Users can also search for dishes and get recommended new dishes. 

#### Category

A Category object describes the `category` of a dish such as Mexican.

#### Restuarant

A Restaurant object describes a restaurant with attributes as `name`, `city`, `state`, `address`, `r_image_link` and `website` infomration.

#### Dish

A Dish object describes a dish with attributes as `name`, `restaurant_id`, `category_id`, `price`, `rating` and `image_link`.

## API endpoints

### Category
The following API allows you to get, post, delete and update categories. You can retrieve a single category or a list of categories from the existing category collection. Only users with admin permissions can create, delete and update category object. Regular users without admin permissions can browse category information.

#### GET '/categories'
- Fetches a list of categories from the existing category collection.
- No request arguments are required.
- Returns a list of id and category pairs.

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
- Retrieves a specified category by `category_id` from the category collection.
- Request arguments: `**category_id**`
- Returns an object with matched category and success status.

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
- Creates a new category in the existing category collection.
- No request arguments are required.
- Data in the body is required.
- Returns a newly added category and success status.

##### Exmaple request with data in the body:
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
- Deletes a specified category based on the `category_id`.
- Request arguments: `**category_id**`
- Returns the `deleted_category_id` and success status.

##### Exmaple request:
`DELETE /categories/3`

##### Exmaple response:

```javascript
{
    "delete_category_id": 3,
    "success": true
}
```

#### PATCH '/categories/{category_id}'
- Requires **Admin** authentication.
- Updates a specified question based on the `category_id`
- Request arguments: `**category_id**`
- Data in the body is required.
- Returns an updated category information and success status.

##### Exmaple request with data in the body:
`PATCH /categories/1`

```javascript
{
	"category": "Chinese"
}
```

##### Exmaple response:
```javascript
{
    "updated category": {
        "category": "Chinese",
        "id": 1
    },
    "success": true
}
```

### Restuarant
The following API allows you to get, post, delete and update restaurants. You can retrieve a single restaurant or a list of restaurants from the existing restaurant collection. Only users with admin permissions can create, delete and update restaurant object. Regular users without admin permissions can browse restaurant information.

#### GET '/restaurants'
- Fetches a list of restaurants from the existing restaurant collection.
- No request arguments are required.
- Returns a list of restaurants including `id`, `name`, `city`, `state`, `address`, `website` and `r_image_link` key:value pairs and success status.

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
- Retrieves a specified restaurant by `restaurant_id` from the restaurant collection.
- Request arguments: `**restaurant_id**`
- Returns a matched restaurant object and success status.

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
- Creates a new restaurant in the existing restaurant collection.
- No request arguments are required.
- Data in the body is required.
- Returns a newly added restaurant and success status.

##### Exmaple request with data in the body:
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
- Deletes a specified restaurant based on the `restaurant_id`.
- Request arguments: `**restaurant_id**`
- Returns the `deleted_restaurant_id` and success status.

##### Exmaple request:
`DELETE /restaurants/2`

##### Exmaple response:

```javascript
{
    "deleted_restaurant_id": 2,
    "success": true
}
```

#### PATCH '/restaurants/{restaurant_id}'
- Requires **Admin** authentication.
- Updates a specified restaurant based on the `restaurant_id`
- Request arguments: `**restaurant_id**`
- Data in the body is required and includes the restaurant's attributes to update.
- Returns a restaurant with the updated attributes and success status.

##### Exmaple request with data in the body:
`PATCH /restaurants/1`

```javascript
{
  "city": "Foster City"
}
```

##### Exmaple response:
```javascript
{
    "updated_restaurant": {
        "address": "Sandwich Monkey address",
        "city": "Foster City",
        "id": 1,
        "name": "Sandwich Monkey",
        "r_image_link": "https://unsplash.com/photos/26T6EAsQCiA",
        "state": "CA",
        "website": "www.sandwichmonkey.com"
    },
    "success": true
}
```

### Dish
The following API allows you to get, post, delete and update dishes. You can retrieve a single dish or a list of dishes from the existing dish collection. Only users with admin permissions can create, delete and update dish object. Regular users without admin permissions can browse dish information. These users can also search for dishes and get recommended new dishes.

#### GET '/dishes'
- Fetches a list of dishes from the existing dish collection.
- No request arguments are required.
- Returns a list of dishes including `id`, `name`, `restaurant_id`, `category_id`, `price`, `rating`, `image_link` key:value pairs and success status.

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
- Retrieves a specified dish by `dish_id` from the dish collection.
- Request arguments: `**dish_id**`
- Returns a matched dish and success status.

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
- Creates a new dish in the existing dish collection.
- No request arguments are required.
- Data in the body is required.
- Returns a newly added dish and success status.

##### Exmaple request with data in the body:
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
- Deletes a specified dish based on the `dish_id`.
- Request arguments: `**dish_id**`
- Returns the `deleted_dish_id` and success status.

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
- Update a specified dish based on the `dish_id`
- Request arguments: `**dish_id**`
- Data in the body is required and includes the dish's attributes to update.
- Returns a dish object with the updated dish information and success status.

##### Exmaple request with data in the body:
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
- Retrieves a list of dishes from the same category by `category_id`
- Request arguments: `**category_id**`
- Returns a list of dishes grouped by a given `category_id` and success status.

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
- Retrieves a list of dishes from the same restaurant by `restaurant_id`
- Request arguments: `**restaurant_id**`
- Returns a list of dishes grouped by a given `restaurant_id` and success status.

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
- Searchs one or a group of dishes by a query string
- No request arguments are required.
- Data in the body is required and includes `search_term` as the key.
- Returns an object with matched dishes and success status.

##### Exmaple request with data in the body:
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

#### POST '/dishes/recommended'
- Fetches a recommended dish with the category that is specified by users and is not from the provided list of the previous dish ids. If no category is specified, then return a dish that is not from the previous dishes and the rating is equal to or greater than 3. If a category is specified, then return a dish that is from the specified category but not from the previous dishes, and the rating is equal to or greater than 3.
- No request arguments are required.
- Data in the body is required and includes a list of previous dish ids and a new catogery id which are provided by users.
- Returns an object with the dish to try and success status.

##### Exmaple request with data in the bdoy:
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
There are two ways to test the app. You can either use test.py or Postman to test APIs. 

#### Test.py
Go to the working directory `FSND2/projects/capstone/05_what_to_eat`, run the following command.

```bash
$ createdb dish_test
$ python3 -m backend.src.test
```

#### Use Postman to test
Role related tokens have been added to the collection file [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat_heroku_deployment.postman_collection.json).
1. Launch Postman.
2. Import the above collection file to Postman.
3. Click the arrow next to the collection name and click Run button.
4. Click Run What_to_eat_heroku_deployment to start the Collection Runner.
4. Check the test results.

#### Retrieve tokens via Auth0
Authentication tokens included in the above collection.json file will expire in 24 hours. Once they expire, please use the following Auth0 link to retrieve the tokens accordingly. 

**Auth0 link**:
https://dev-auth2.auth0.com/authorize?audience=Dishes&response_type=token&client_id=eCc4Btc6EONcULa1scEWiIB32x3PZxBd&redirect_uri=https://127.0.0.1:8080/login

**Admin login**: cumulus166@gmail.com / password: Coffee123@@

**User login**: cumulus189@gmail.com / password: Coffee123@@

Valid tokens are required before using the app. Open Postman -> What_to_eat_heroku_deployment -> Admin -> Edit -> Authorization tab, update the old token with the new token in the Token section. Under User folder in Postman, follow the same steps to update User's token in Postman. Then you should be able test the app in different roles.