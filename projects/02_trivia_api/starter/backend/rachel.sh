#!/bin/sh -x

cd /Users/rachel/full_stack_class/projects/fyyur/FSND/projects/02_trivia_api/starter/backend
# dropdb trivia
# createdb trivia
dropdb trivia_test
createdb trivia_test
psql -U Rachel -d trivia_test -a -f trivia.psql
rm -rf migrations
flask db init
flask db stamp head
flask db migrate # from flask_migrate import Migrate, migrate = Migrate(app, db) 
flask db upgrade
psql trivia -c '\dt'
psql trivia -c 'select * from questions'
psql trivia -c 'select * from categories'

PGGSSENCMODE=disable FLASK_APP=./flaskr/app.py FLASK_DEBUG=TRUE flask run