import os
from alembic.config import Config
#from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, MetaData
from sqlalchemydiff.util import (
    destroy_database,
    get_temporary_uri,
    new_db,
)

from utils import get_config



def include_url_to_config(config):
    config.set_main_option("sqlalchemy.url", get_config('SQLALCHEMY_DATABASE_URI'))
    return config


def create_temp_config(app):
    """Create alembic config with temp DB."""

    uri = app.config['SQLALCHEMY_DATABASE_URI']
    config_dir = os.path.abspath(os.path.dirname('migrations/'))
    config = Config(os.path.join(config_dir, 'alembic.ini'))

    uri_temp = get_temporary_uri(uri)

    config.set_main_option("script_location", config_dir)
    config.set_main_option("sqlalchemy.url", uri_temp)

    return config


class DBTemp():
    """Test database migrations."""

    def __init__(self, app):
        self.app = app
        self.config = create_temp_config(app)
        config_ini_section = self.config.config_ini_section
        self.uri = self.config.file_config.get(config_ini_section, 'sqlalchemy.url')
        self.db_exist = False
        self.engine = None
        self.metadata = None
        self.script = ScriptDirectory.from_config(self.config)

    def base_from_models(self):

        assert not self.db_exist

        new_db(self.uri)

        self.engine = create_engine(self.uri)
        #self.engine.execute("CREATE EXTENSION pgcrypto;")

        db = self.app.extensions.get('sqlalchemy').db

        db.metadata.create_all(self.engine)

        self.metadata = MetaData(bind=self.engine)
        self.metadata.reflect()
        self.metadata.bind = None
        self.db_exist = True

    # def base_from_migrations(self):
    #
    #     assert not self.db_exist
    #
    #     new_db(self.uri)
    #
    #     command.upgrade(self.config, 'head')
    #
    #     self.engine = create_engine(self.uri)
    #     self.metadata = MetaData(bind=self.engine)
    #     self.metadata.reflect()
    #     self.metadata.bind = None
    #     self.db_exist = True

    def destroy_base(self):
        destroy_database(self.uri)
        self.db_exist = False
        self.engine = None
        self.metadata = None


def metadata_from_models(app):
    base = DBTemp(app)
    base.base_from_models()
    metadata = base.metadata
    base.destroy_base()
    return metadata
