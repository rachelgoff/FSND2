#!/bin/sh -x

# dropdb dish
createdb dish
export DATABASE_URL='postgresql://localhost:5432/dish' 
export PGGSSENCMODE=disable 
export FLASK_APP=backend/src/app.py 
export FLASK_ENV=development 
flask run