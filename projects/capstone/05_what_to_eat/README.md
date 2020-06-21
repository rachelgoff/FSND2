# Welcome to the What To Eat Backend

This app works as a meal planner for users. It gives users suggestions based on their previous favorite take-out food items from various restaurants. It saves users' time and energy to plan their meals. Especially when the restaurants are not fully opened with their sitting down area during this particular situation, users will spend lots of time on eating at home. The What To Eat app will plan users' meals with the food they used to love. Using What To Eat, your favorite food is just one button away. In the current version, users will be able to view the recommended dishes. Ordering feature will be available in the future versions.

## Virtual environment

Virtual environment is highly recommended. Instructions for setting up virtual environment can be found at: [Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments).

Go to the working directory `FSND2/projects/capstone/05_what_to_eat`, and set up virtual environment on MacOS and Linux by following the steps below. For other platforms, please refer to the link above.

```bash
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
$ source env/bin/activate
```

To deactivate a virutal environment:
```bash
$ deactivate
```

## PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `FSND2/projects/capstone/05_what_to_eat` directory and running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages which are selected within the `requirements.txt` file.

## Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [PostgresSQL](https://www.postgresql.org/download/) is a powerful, open source object-relational database system.

## Working Directory
Go to the directory where you check out the [repository](https://github.com/rachelgoff/FSND2) which includes What To Eat backend code. The working directory is under `FSND2/projects/capstone/05_what_to_eat`.

## Running the server

### Running the server from localhost
Make sure you are working using your created virtual environment and **PostgreSQL** is running on port 5432 before you start running the server. Go to the working directory `FSND2/projects/capstone/05_what_to_eat`, then run the following command:

or you can run `setup.sh` from the working directory. 
```bash
$ chmod +x setup.sh
$ ./setup.sh
```

### Deployment on Heroku
The app's backend server is deployed on Heroku. You can visit and interact with the app's backend server via: 

https://what-to-eat-by-rg.herokuapp.com/. 

Please note that the frontend code is not available yet. In order to test the APIs, please use Postman with proper authentication information. For Postman, the authentication tokens have been included in [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat_heroku_deployment.postman_collection.json). Feel free to download this collection.json file and import it in Postman before testing APIs. 

To import the collection.json file, you can launch Postman - click Import button on the top left corner - Choose Files - Import. The default host is set to http://127.0.0.1:5000 in the collection variables. If you want to test APIs with Heroku deployment, you can update the collection variable `WTE_URL` to https://what-to-eat-by-rg.herokuapp.com/ in Postman.

## Data modeling
**model.py** includes database schema and helper functions such as insert, update, delete and format functions. There are three tables created in the database: **categories**, **restaurants** and **dishes**. Only Admin users can create, update and delete entries from the tables. Regular users can only view the entries in the three tables. Users can also search for dishes and get recommended new dishes. 

#### Category

A Category object describes the `category` of a dish such as Mexican.

#### Restuarant

A Restaurant object describes a restaurant with attributes as `name`, `city`, `state`, `address`, `r_image_link` and `website` infomration.

#### Dish

A Dish object describes a dish with attributes as `name`, `restaurant_id`, `category_id`, `price`, `rating` and `image_link`.

## API use cases

### Admin
* Only users with **admin token** have all the admin permissions. Refer to **Retrieve tokens via Auth0** section below which mentions how to retrive admin token. Please note that Admin users have to create categories, restaurants and dishes first before users can view the related content in the app.
* Admin users can create a new category, a new restaurant and a new dish via `POST /categories`, `POST /restaurants`, `POST /dishes` respectively. Please note that because of the relationship, a category and a restaurant have to be created first before creating a dish.
* Admin users can delete a cateogry, a restaurant and a dish via `DELETE /categories/{category_id}`, `DELETE /restaurants/{restaurant_id}`, `DELETE /dishes/{dish_id}` respectively.
* Admin users can update a cateogry, a restaurant and a dish via `PATCH /categories/{category_id}`, `PATCH /restaurants/{restaurant_id}`, `PATCH /dishes/{dish_id}` respectively.
* All the users' use cases below apply to Admin users.

### User
* Users can view lists of categories, restaurants and dishes via `GET /categories`, `GET /restaurants`, `GET /dishes` respectively.
* Users can view a list of dishes from a specified category via `GET /categories/{category_id}/dishes`.
* Users can view a list of dishes from a specified restaurant via `GET /restaurants/{restaurant_id}/dishes`.
* Users can search dishes using search terms via `POST /dishes/search`. The search is case insesitive. For example, when users search "Sandwich", they will see either "Sandwich" or "sandwiches" in the search result.
* Users can browse recommended dishes via `POST /dishes/recommended`. Users will need to privode the previous dishes they had, and optionally a new dish category the users would like to try. Then users can view a recommend dish which is not from the previous dish list. If no new dish category is specified, the app will recommend a dish from any category but not from the previous dish list. All the recommended dishes rating is equal to or greater than 3. 

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
            "id": 1,
            "name": "Mexican"
        },
        {
            "id": 2,
            "name": "American"
        }
    ],
    "success": true
}
```

#### GET '/categories/{category_id}'
- Retrieves a specified category by `category_id` from the category collection.
- Request arguments: `category_id`
- Returns an object with matched category and success status.

##### Exmaple request:
`GET /categories/1`

##### Exmaple response:

```javascript
{
    "category": {
        "id": 1,
        "name": "Mexican"
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
	"name": "Chinese"
}
```

##### Exmaple response:
```javascript
{
    "category": {
        "id": 3,
        "name": "Chinese"
    },
    "success": true
}
```

#### DELETE '/categories/{category_id}'
- Requires **Admin** authentication.
- Deletes a specified category based on the `category_id`.
- Request arguments: `category_id`
- Returns the deleted `category` and success status.

##### Exmaple request:
`DELETE /categories/3`

##### Exmaple response:

```javascript
{
    "category": {
        "id": 3
    },
    "success": true
}
```

#### PATCH '/categories/{category_id}'
- Requires **Admin** authentication.
- Updates a specified question based on the `category_id`
- Request arguments: `category_id`
- Data in the body is required.
- Returns an updated category information and success status.

##### Exmaple request with data in the body:
`PATCH /categories/1`

```javascript
{
	"name": "Chinese"
}
```

##### Exmaple response:
```javascript
{
    "category": {
        "id": 1,
        "name": "Chinese"
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
- Request arguments: `restaurant_id`
- Returns a matched restaurant and success status.

##### Exmaple request:
`GET /restaurants/1`

##### Exmaple response:

```javascript
{
    "restaurant": {
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
    "restaurant": {
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
- Request arguments: `restaurant_id`
- Returns the deleted `restaurant` and success status.

##### Exmaple request:
`DELETE /restaurants/2`

##### Exmaple response:

```javascript
{
    "restaurant": {
        "id": 2
    },
    "success": true
}
```

#### PATCH '/restaurants/{restaurant_id}'
- Requires **Admin** authentication.
- Updates a specified restaurant based on the `restaurant_id`
- Request arguments: `restaurant_id`
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
    "restaurant": {
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
- Request arguments: `dish_id`
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
    "dish": {
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
- Request arguments: `dish_id`
- Returns the deleted `dish` and success status.

##### Exmaple request:
`DELETE /dishes/3`

##### Exmaple response:

```javascript
{
    "dish": {
        "id": 3
    },
    "success": true
}
```

#### PATCH '/dishes/{dish_id}'
- Requires **Admin** authentication.
- Update a specified dish based on the `dish_id`
- Request arguments: `dish_id`
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
- Request arguments: `category_id`
- Returns a list of dishes grouped by a given `category_id` and success status.

##### Exmaple request:
`GET /categories/2/dishes`

##### Exmaple response:
```javascript
{
    "dishes": [
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
- Request arguments: `restaurant_id`
- Returns a list of dishes grouped by a given `restaurant_id` and success status.

##### Exmaple request:
`GET /restaurants/1/dishes`

##### Exmaple response:
```javascript
{
    "dishes": [
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
- Data in the body is required and includes a list of previous `dish_id` and a new `catogery_id` which are provided by users.
- Returns a recommended dish and success status.

##### Exmaple request with data in the bdoy:
`POST /dishes/recommended`

```javascript
{
	"previous_dishes": [4],
	"new_category":2
}
```

##### Exmaple response:
```javascript
{
    "dish": {
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

### Test.py
In order to test the backend server, go to the working directory `FSND2/projects/capstone/05_what_to_eat`, run the following command.

```bash
$ chmod +x test_setup.sh
$ ./test_setup.sh
```

### Retrieve tokens via Auth0
Authentication tokens included in **test_setup.sh** and [What_to_eat_heroku_deployment.postman_collection.json](https://github.com/rachelgoff/FSND2/blob/master/projects/capstone/05_what_to_eat/What_to_eat_heroku_deployment.postman_collection.json) will expire in **24** hours. Once the tokens expire, please use the following Auth0 link to retrieve the updated tokens accordingly. 

**Auth0 link**:
https://dev-auth2.auth0.com/authorize?audience=Dishes&response_type=token&client_id=eCc4Btc6EONcULa1scEWiIB32x3PZxBd&redirect_uri=https://127.0.0.1:5000/login

**Admin login**: cumulus166@gmail.com / password: Coffee123@@

**User login**: cumulus189@gmail.com / password: Coffee123@@

Make sure you clear the browser cache before you login with link above. After you login, you will see the following link as the browser address. The token is the value of "access_token". So copy the value between "access_token=" and "&expires_in=86400&token_type=Bearer". That's the token we use in Postman and test_setup.sh.

For example, the token we are looking for is `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkyNjAzODEwLCJleHAiOjE1OTI2OTAyMTAsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.ft2me_AL3-ByK2l0wK2PrHbD7Ml8T7Jc-gKsu9tOhyDcB5EqqNbGRdgT_phgZ2dTeD0NUvndbsa7UJdFFDJ_JkvCA7dntQeXgw5tZ-OfBPiI5q0E5dij78D1zd6h9ysRSVvc9qwaENCwovFmWE_OvKIsP0Bqeb2RSiLrATVupFa_JSY8tNP2m9fCKtTFP-C0l5iJa6VU_kC-NpRHrOjBr8peXJ0zPqqiNyzDHdn8nDNkCNuF3a3jV_GMbrr5Ek8OVtzuHBO4wJEG-n1905vlhHbrHbNER2Lmw8Lwzka8zi2QMRGcIbjdYKcj0xfoMLKpVtcu-s2-LBNbxTQ93jG4NA`,

which is from the link:
https://127.0.0.1:5000/login#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56RXpNemt6UmtFMVFrTkdSREF5TkRJek1Ea3hSRGhFT1RJNFJFWTJNek5HUWtaRFJUY3dSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hdXRoMi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2NDg2NDVjNmRiYzkwZDNkZTJkMDdjIiwiYXVkIjoiRGlzaGVzIiwiaWF0IjoxNTkyNjAzODEwLCJleHAiOjE1OTI2OTAyMTAsImF6cCI6ImVDYzRCdGM2RU9OY1VMYTFzY0VXaUlCMzJ4M1BaeEJkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTpkaXNoZXMiLCJkZWxldGU6cmVzdGF1cmFudHMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpkaXNoZXMiLCJnZXQ6cmVzdGF1cmFudHMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6ZGlzaGVzIiwicGF0Y2g6cmVzdGF1cmFudHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRpc2hlcyIsInBvc3Q6cmVzdGF1cmFudHMiXX0.ft2me_AL3-ByK2l0wK2PrHbD7Ml8T7Jc-gKsu9tOhyDcB5EqqNbGRdgT_phgZ2dTeD0NUvndbsa7UJdFFDJ_JkvCA7dntQeXgw5tZ-OfBPiI5q0E5dij78D1zd6h9ysRSVvc9qwaENCwovFmWE_OvKIsP0Bqeb2RSiLrATVupFa_JSY8tNP2m9fCKtTFP-C0l5iJa6VU_kC-NpRHrOjBr8peXJ0zPqqiNyzDHdn8nDNkCNuF3a3jV_GMbrr5Ek8OVtzuHBO4wJEG-n1905vlhHbrHbNER2Lmw8Lwzka8zi2QMRGcIbjdYKcj0xfoMLKpVtcu-s2-LBNbxTQ93jG4NA&expires_in=86400&token_type=Bearer

Valid tokens are required before using the app. Open Postman -> What_to_eat_heroku_deployment -> Admin -> Edit -> Authorization tab, update the old token with the new token in the Token section. Under User folder in Postman, follow the same steps to update User's token in Postman. Then you should be able test the app in different roles.