#!/usr/bin/python3
"""Tool for manage project."""
from shutil import rmtree
from pathlib import Path
import os
import subprocess

from src import create_app
from src.db import db
from src.lib.db import include_url_to_config
from src.lib.utils import get_config
from src.tests import run_unit_tests
from src.db.fixtures import create_fixtures, params_fixtures
from src.lib.context import shel_context
from src.lib.mail_parser import get_email
from flask_script import Manager, Command, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
migrate = Migrate(app, db)
migrate.configure_callbacks.append(include_url_to_config)

def run():
    if get_config('DEBUG'):
        app.run(
            debug=app.config['DEBUG'],
            host=app.config['HOST'],
            port=app.config['PORT'],
            threaded=False,
            processes=3
        )
    else:
        subprocess.call(
            ['gunicorn',
             '--access-logfile',
             '-',
             '--workers=25',
             '--timeout=600',
             '--bind',
             '0.0.0.0:5000',
             'manage:app']
        )


manager = Manager(app, with_default_commands=False, usage='Manage flask_api instance')

tests_command = Command(run_unit_tests)
tests_command.option_list[0].kwargs['nargs'] = '*'

manager.add_command('db', MigrateCommand)
manager.add_command("run", Command(run))
manager.add_command("fix", Command(create_fixtures))
manager.add_command("fix1", Command(params_fixtures))
manager.add_command("test", tests_command)
manager.add_command("shell", Shell(make_context=shel_context))
manager.add_command("getemail", Command(get_email))

if __name__ == '__main__':
    manager.run()
