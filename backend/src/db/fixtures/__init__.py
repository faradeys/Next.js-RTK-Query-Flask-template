"""fixtures."""
from flask import current_app as app

from src.db.models import ServiceParams, User, Role, Prices
from src.db import session
from src.lib.utils import parse_phone


def create_fixtures():
    """Create fixtures."""
    users = app.config['FIXTURE_USERS']
    user = users.get('test_user')
    admin = users.get('admin')

    fixtures = []

    # Roles
    role_all = Role(name="all")

    role_user = Role(name="user")
    role_user.add_parent(role_all)

    role_admin = Role(name="admin")
    role_admin.add_parent(role_all)
    role_admin.add_parent(role_user)

    fixtures.extend([role_all, role_user, role_admin])

    # Users
    user_admin = User(name="admin", email=admin.get('email'), phone=admin.get('phone'), is_verified=True)
    user_admin.hash_password(admin.get('password'))
    user_admin.add_role(role_admin)
    
    test_user = User(name="user", email=user.get('email'), phone=user.get('phone'), is_verified=True)
    test_user.hash_password(user.get('password'))
    test_user.add_role(role_user)

    fixtures.extend([user_admin, test_user])

    session.add_all(fixtures)
    session.commit()
    print('DONE!!!')

def params_fixtures():
    fixtures = []

    if fixtures:
        print('-> d offers update (DONT RUN IT TWICE!!!!)')
        session.add_all(fixtures)
        session.commit()

    print('== DONE!')
