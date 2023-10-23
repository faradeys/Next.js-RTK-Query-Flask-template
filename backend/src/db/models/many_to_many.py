"""many_to_many model."""
from src.db import db
from sqlalchemy.dialects.postgresql import UUID

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', UUID, db.ForeignKey('users.id')),
    db.Column('role_id', db.INTEGER, db.ForeignKey('roles.id'))
)

roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.INTEGER, db.ForeignKey('roles.id')),
    db.Column('parent_id', db.INTEGER, db.ForeignKey('roles.id'))
)