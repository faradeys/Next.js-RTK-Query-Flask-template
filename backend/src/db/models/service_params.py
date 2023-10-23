from src.db import db
from sqlalchemy.dialects.postgresql import UUID


class ServiceParams(db.Model):
    __tablename__ = 'service_params'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    parent_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    parent = db.relationship('ServiceParams', remote_side=[id])
    childs = db.relationship('ServiceParams', remote_side=[parent_id])
    name = db.Column(db.VARCHAR(256))
    u_name = db.Column(db.VARCHAR(256))
    spec_value = db.Column(db.VARCHAR(256))
    deprecated = db.Column(db.BOOLEAN, default=False, server_default=db.text('False'))
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    update_at = db.Column(db.TIMESTAMP(timezone=True),
                          server_default=db.text('now()::timestamp(0)'))

    def find_child(self, child):
        return ServiceParams.get_by_uname(child, group_id=self.id)

    @staticmethod
    def get_by_uname(param=None, group=None, group_id=None):
        if not group:
            if group_id:
                return ServiceParams.query.filter_by(u_name=str(param), deprecated=False).filter(ServiceParams.parent.has(id=str(group_id))).first()
            return ServiceParams.query.filter_by(u_name=str(param), deprecated=False).first()
        if not param:
            return ServiceParams.query.filter(ServiceParams.parent.has(u_name=str(group)), ServiceParams.deprecated==False).all()
        return ServiceParams.query.filter_by(u_name=str(param), deprecated=False).filter(ServiceParams.parent.has(u_name=str(group))).first()
