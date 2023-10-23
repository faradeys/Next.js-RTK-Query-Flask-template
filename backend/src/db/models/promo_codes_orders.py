from src.db import db
from sqlalchemy.dialects.postgresql import UUID


class PromoCodesOrders(db.Model):
    __tablename__ = 'promo_codes_orders'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    order_id = db.Column(UUID, db.ForeignKey('orders.id'))
    order = db.relationship('Orders', foreign_keys=[order_id])
    promo_code_id = db.Column(UUID, db.ForeignKey('promo_codes.id'))
    promo_code = db.relationship('PromoCodes', foreign_keys=[promo_code_id])
    price = db.Column(db.INTEGER, default=0, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))