from flask import g
from src.db import db, session
from sqlalchemy.dialects.postgresql import UUID


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    customer_id = db.Column(UUID, db.ForeignKey('users.id'))
    customer = db.relationship('User')
    name = db.Column(db.VARCHAR(255))
    phone = db.Column(db.VARCHAR(50))
    price = db.Column(db.VARCHAR(50))
    city = db.Column(db.VARCHAR(150))
    model_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    model = db.relationship('ServiceParams', foreign_keys=[model_id])
    ordered_damages = db.Column(db.TEXT)
    ordered_problems = db.Column(db.TEXT)
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    update_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))

    @staticmethod
    def get_all():
        return Orders.query.filter_by(customer_id=g.current_user.id).order_by(Orders.created_at.desc()).all()

    @staticmethod
    def get_one_own(order_id):
        return Orders.query.filter_by(customer_id=g.current_user.id, id=order_id).first()

    @staticmethod
    def parse_old_entries(phone, user):
        old_orders = Orders.query.filter_by(phone=phone, customer_id=None).all()
        if old_orders:
            for order in old_orders:
                order.customer = user
            session.commit()

    @property
    def order_info(self):
            # if self.ordered_service.ger_prices_dict[self.selected_price_type]:
            #     if self.sale:
            #         selected_price = self.ordered_service.ger_prices_dict[self.selected_price_type] - self.ordered_service.ger_prices_dict['sale']
            #     else:
            #         selected_price = self.ordered_service.ger_prices_dict[self.selected_price_type]

        return {
            'name': self.name,
            'phone': self.phone,
            'model': self.model.name,
            'damages': self.ordered_damages,
            'problems': self.ordered_problems,
            'price': self.price,
        }

    @property
    def order_type(self):
        return 'phone_repair'
