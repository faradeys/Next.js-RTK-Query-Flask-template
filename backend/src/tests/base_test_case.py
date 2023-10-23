"""Наш внутренний тесткейс,
инициализирует свою базу данных и свое приложение."""
import os
import pprint

import requests
from flask import Flask
from flask_testing import LiveServerTestCase
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemydiff.util import (
    destroy_database,
    get_temporary_uri,
    new_db,
    prepare_schema_from_models,
)

from src.app import create_app
from src.db import Base, fdb
from src.db.models import ALL_MODELS

from utils import get_config


class CaseSkeleton(LiveServerTestCase):
    """
    Родительский класс для тестов,
    требующих своего приложения и своей базы.
    """
    testdb_uri = None

    def create_app(self):
        """
        Переопределние метода create_app из LiveServerTestCase.

        Для того чтобы скормить тестам наше приложение.
        """
        uri = (get_config('DB_CONFIG'))
        self.testdb_uri = get_temporary_uri(uri)
        new_db(self.testdb_uri)
        engine = create_engine(self.testdb_uri)
        engine.execute("CREATE EXTENSION pgcrypto;")
        prepare_schema_from_models(self.testdb_uri, Base)
        app = create_app(self.testdb_uri)
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def tearDown(self):
        """
        Единый tearDown для всех наших тестов, требующих отдельных баз.

        Должен сносить все состояние в т.ч. из редиса если тесты с
        участием редиса замаячат на горизонте.
        """
        fdb.session.remove()
        destroy_database(self.testdb_uri)
