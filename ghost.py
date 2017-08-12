import os
from app.app import factory


ghost = factory(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    ghost.run()