#!/bin/sh -x

# create database with name as dish
# dropdb dish
createdb dish

# Export the environment variables and set up for the server
export DATABASE_URL='postgresql://localhost:5432/dish' 
export PGGSSENCMODE=disable 
export FLASK_APP=backend/src/app.py 
export FLASK_ENV=development 
flask run