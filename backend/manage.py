
from flask_vue_jquery_deskapp.app import create_app, db
from flask_vue_jquery_deskapp.app import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# @manager.command
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()


# python3 manage.py db init
# python3 manage.py db migrate -m 'initial migration'
# python3 manage.py db upgrade
# python3 manage.py db downgrade commit_id