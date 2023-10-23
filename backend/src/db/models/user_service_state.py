from flask import g
from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import JSONType
from sqlalchemy_json import NestedMutable

from . import ServiceParams


class UserServiceState(db.Model):
    __tablename__ = 'user_service_states'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('users.id'))
    user = db.relationship('User')
    service_type_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    service_type = db.relationship('ServiceParams')
    json_data = db.Column(NestedMutable.as_mutable(JSONType))


    @classmethod
    def get_or_create(cls, service_type_name, json_data):
        service_type = ServiceParams.get_by_uname(service_type_name)
        if not service_type:
            return False

        obj = cls(
            service_type = service_type,
            user = g.current_user,
            json_data = json_data
        )
        db.session.add(obj)
        db.session.commit()

        return obj.id
