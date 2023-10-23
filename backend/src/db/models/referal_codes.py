import random, string
from src.db import db
from sqlalchemy.dialects.postgresql import UUID

from . import ServiceParams


class ReferalCode(db.Model):
    __tablename__ = 'referal_codes'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    service_type_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    service_type = db.relationship('ServiceParams')
    referrer_name = db.Column(db.VARCHAR(100))
    referrer_phone = db.Column(db.VARCHAR(50))
    invite_by_sms = db.Column(db.BOOLEAN, default=False)
    code = db.Column(db.VARCHAR(10))
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.text('now()::timestamp(0)'))


    @staticmethod
    def find(referal_code):
        referrer = ReferalCode.query.filter_by(code=referal_code).first()
        if referrer:
            return referrer


    @classmethod
    def new_one(cls, referrer_name, referrer_phone, service_type_name):
        service_type = ServiceParams.get_by_uname(str(service_type_name))
        if not service_type:
            print('===NO SUCH SERVICE TYPE===')
            return None

        obj = cls(
            service_type = service_type,
            referrer_name = referrer_name,
            referrer_phone = referrer_phone,
            code = cls.generate_code()
        )

        db.session.add(obj)
        db.session.commit()

        return obj.code


    @classmethod
    def generate_code(cls):
        referal_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
        existed_ref = ReferalCode.query.filter_by(code=referal_code).first()
        if existed_ref:
            return cls.generate_code()
        else:
            return referal_code
