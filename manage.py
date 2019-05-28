import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.main import createApp, db
from app import blueprint

# init the app with an environment set by our environment flags, or dev by default.
app = createApp(os.getenv('FLASK_ENV') or 'development')
app.register_blueprint(blueprint)

# The app context is a reference to currently running Flask app. According to Flask's documentation, web request 
# objects may not always be thread safe since they may use the same thread, if running Flask with multiple threads. 
# app contexts and request contexts save the information on a stack to avoid this problem. It also allows the object(s)
# to be treated globally rather than being chained through functions, which is how Node/Express does things. 
app.app_context().push()

# Instantiate a script manager.
manager = Manager(app)

# Instantiate a DB patcher, and add the db command. 
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

port = os.getenv('PORT') or 5000
host = os.getenv('HOST') or '0.0.0.0'

"""
`run` - starts the backend.
"""
@manager.command
def run():
    app.run()

"""
`test` - runs unit tests.
"""
@manager.command
def test():
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run(host, port)