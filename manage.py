from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Movie, Actor, movies

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    Movie(title='Lion King', release_date='2012-1-1').insert()
    Movie(title='Joker', release_date='2019-8-12').insert()
    Movie(title='Frozen', release_date='2011-12-12').insert()

    Actor(name='Edward', age=36, gender='male').insert()
    Actor(name='David', age=25, gender='other').insert()
    Actor(name='Jeff', age=35, gender='female').insert()
    
   
if __name__ == '__main__':
    manager.run()