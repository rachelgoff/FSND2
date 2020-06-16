
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

'''
Import modules from the relative directory
'''
from backend.src.app import create_app 
from backend.src.database.models import db

migrate = Migrate(create_app, db)
manager = Manager(create_app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

