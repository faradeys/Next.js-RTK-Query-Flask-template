"""User model."""
import random, string
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from simple_storage import FileStorage

from src.db import db, session
from src.db.models.many_to_many import users_roles
from src.lib.access import generate_token, verify_token, login_manager
from src.lib.sending import send_sms
from .orders import Orders
from .role import Role
from . import ReferalCode
from . import ServiceParams

class User(db.Model):
    """Base user model class."""

    __tablename__ = 'users'

    # identification
    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    side_id = db.Column(db.VARCHAR(150))
    roles = db.relationship('Role', secondary=users_roles)
    bonuses = db.Column(db.INTEGER, server_default=db.text('0'))
    name = db.Column(db.VARCHAR(256))
    city = db.Column(db.VARCHAR(200))
    email = db.Column(db.VARCHAR(160))
    phone = db.Column(db.VARCHAR(50), index=True)
    password = db.Column(db.VARCHAR(256))

    # Statuses
    is_verified = db.Column(db.BOOLEAN, default=False)
    is_banned = db.Column(db.BOOLEAN, default=False)
    banned_at = db.Column(db.TIMESTAMP(timezone=True))
    is_deleted = db.Column(db.BOOLEAN, default=False)
    deleted_at = db.Column(db.TIMESTAMP(timezone=True))
    avatar_id = db.Column(UUID, db.ForeignKey('files.id'))
    avatar = db.relationship('File', foreign_keys=[avatar_id])

    # Tech info
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    update_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    bonuses_add_at = db.Column(db.TIMESTAMP(timezone=True))

    # Referal info
    referrers_id = db.Column(UUID, db.ForeignKey('users.id'))
    referrer_status =  db.Column(db.BOOLEAN, default=False)
    self_referal_code = db.Column(db.VARCHAR(10))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return not self.is_banned

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def avatar_path(self):
        if self.avatar:
            return self.avatar.absolute_path()
        return None

    # role functions
    @property
    def role(self):
        if self.roles:
            return self.roles[0].name

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def roles_all(self):
        result = []
        for role in self.roles:
            result.extend(role.roles_all())
        return result

    def verify_access(self, role_name):
        if role_name in [x.name for x in self.roles_all()]:
            return True  # valid role
        else:
            return False  # invalid role

    # password functions
    def hash_password(self, password=None):
        if not password:
            password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])  # generate rand password

        self.password = generate_password_hash(str(password), method='pbkdf2:sha256', salt_length=15)
        return str(password)

    def verify_password(self, recieved_password):
        if self.password:
            return check_password_hash(self.password, recieved_password)
        return False

    # token finctions
    def generate_auth_token(self):
        return generate_token(self.id)

    @property
    def referal_code(self):
        if not self.self_referal_code:
            no_tradein_order_sp = ServiceParams.get_by_uname('no_tradein_order')
            if not isinstance(no_tradein_order_sp, ServiceParams):
                return None

            self.self_referal_code = ReferalCode.new_one(
                referrer_name=self.name,
                referrer_phone=self.phone,
                service_type_name=no_tradein_order_sp.u_name
            )
            session.commit()

        return self.self_referal_code

    @staticmethod
    def verify_auth_token(token):
        token_claimset = verify_token(token)
        if not token_claimset:
            return None
        current_user = User.query.get(token_claimset['uid'])

        return current_user

    @staticmethod
    def check_phone_number(phone, verified=False):
        filters = {'phone': str(phone)}
        if verified:
            filters.update({'is_verified': True})
        user = User.query.filter_by(**filters).first()
        if user:
            return user
        return None

    @staticmethod
    def new_one(phone, verified=True):
        user = User(
            phone=phone,
            is_verified=verified
        )
        user.add_role(Role.get_by_name('user'))
        session.add(user)
        session.commit()

        return user

    def bonus_top_up(self, value):
        self.bonuses += int(value)
        self.bonuses_add_at = db.text('now()::timestamp(0)')

    def bonus_charge_off(self, value):
        if self.bonuses < int(value):
            return False
        self.bonuses - int(value)
        return True

    # ban function
    def ban(self):
        self.is_banned = True
        self.banned_at = db.text('now()::timestamp(0)')
        db.session.commit()

    def ban_recovery(self):
        self.is_banned = False
        self.banned_at = None
        db.session.commit()

    # delete function
    def delete(self):
        self.is_deleted = True
        self.deleted_at = db.text('now()::timestamp(0)')
        db.session.commit()

    def recovery(self):
        self.is_deleted = False
        self.deleted_at = None
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id, is_deleted=False).first()
