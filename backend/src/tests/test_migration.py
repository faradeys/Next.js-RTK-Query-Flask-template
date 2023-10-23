# pylama:ignore=W0611
"""Migration testing."""
import os
import unittest
import pprint

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemydiff import compare
from sqlalchemydiff.util import (
    destroy_database,
    get_temporary_uri,
    new_db,
    prepare_schema_from_models,
)

from alembicverify.util import (
    get_current_revision,
    get_head_revision,
    make_alembic_config,
    prepare_schema_from_migrations,
)
from src.db import db


from utils import get_config

alembic_root = os.path.abspath(os.path.join('migrations'))


class TestMigration(unittest.TestCase):
    """Test database migrations."""

    def setUp(self):
        """Test setup."""
        uri = (get_config('SQLALCHEMY_DATABASE_URI'))
        alembic_ini = os.path.abspath('migrations/alembic.ini')

        self.uri_left = get_temporary_uri(uri)
        self.uri_right = get_temporary_uri(uri)

        self.alembic_config_left = Config(alembic_ini)
        self.alembic_config_left.set_main_option("script_location",
                                                 alembic_root)
        self.alembic_config_left.set_main_option("sqlalchemy.url",
                                                 self.uri_left)

        self.alembic_config_right = Config(alembic_ini)
        self.alembic_config_right.set_main_option("script_location",
                                                  alembic_root)
        self.alembic_config_right.set_main_option("sqlalchemy.url",
                                                  self.uri_right)

        new_db(self.uri_left)
        new_db(self.uri_right)

    def tearDown(self):
        """To be executed after test."""
        destroy_database(self.uri_left)
        destroy_database(self.uri_right)

    def test_upgrade_and_downgrade(self):
        """
        Test all migrations up and down.

        Tests that we can apply all migrations from a brand new empty
        database, and also that we can remove them all.
        """
        engine, script = prepare_schema_from_migrations(
            self.uri_left, self.alembic_config_left)

        head = get_head_revision(self.alembic_config_left, engine, script)
        current = get_current_revision(
            self.alembic_config_left, engine, script)

        assert head == current

        while current is not None:
            command.downgrade(self.alembic_config_left, '-1')
            current = get_current_revision(
                self.alembic_config_left, engine, script)

    def test_model_and_migration_schemas_are_the_same(self):
        """
        Compare two databases.

        Compares the database obtained with all migrations against the
        one we get out of the models.  It produces a text file with the
        results to help debug differences.
        """
        prepare_schema_from_migrations(self.uri_left, self.alembic_config_left)

        engine = create_engine(self.uri_right)
        engine.execute("CREATE EXTENSION pgcrypto;")
        engine.execute("CREATE EXTENSION postgis;")
        engine.execute("CREATE EXTENSION postgis_topology;")
        engine.execute("CREATE EXTENSION postgis_sfcgal;")
        engine.execute("CREATE EXTENSION fuzzystrmatch;")
        engine.execute("CREATE EXTENSION postgis_tiger_geocoder;")

        prepare_schema_from_models(self.uri_right, db)

        result = compare(
            self.uri_left, self.uri_right, set(['alembic_version']))

        if not result.is_match:
            print("###### DB MISMATCH:")
            pprint.PrettyPrinter(indent=1).pprint(result.errors)

        assert result.is_match
