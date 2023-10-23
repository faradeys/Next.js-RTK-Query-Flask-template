"""Initialization of database."""
from flask_sqlalchemy import SQLAlchemy as SA
from redis import Redis
from src.lib.utils import get_config

class SQLAlchemy(SA):
    def apply_pool_defaults(self, app, options):
        SA.apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()
session = db.session
redis = Redis( get_config('REDIS_HOST'), db=0 )

def get_class_by_tablename(table_fullname):
  for c in db.Model._decl_class_registry.values():
    if hasattr(c, '__table__') and c.__table__.fullname == table_fullname:
      return c

from src.db import models
