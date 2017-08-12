from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.app import factory
from app.extensions import db

app = factory()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
