from src.db import db
from sqlalchemy.dialects.postgresql import UUID


class PromoCodes(db.Model):
    __tablename__ = 'promo_codes'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    code = db.Column(db.TEXT)
    type = db.Column(UUID)
    order_type = db.Column(db.TEXT)
    started_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    ends_at = db.Column(db.TIMESTAMP(timezone=True))
    price = db.Column(db.INTEGER, default=0, nullable=False)
    min_price = db.Column(db.INTEGER)
    max_price = db.Column(db.INTEGER)
    active = db.Column(db.BOOLEAN, default=True,
                       server_default=db.text('True'))
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))

    @staticmethod
    def find(promo_code):
        code = PromoCodes.query.filter_by(code=promo_code, active=True).all()
        if code:
            return code