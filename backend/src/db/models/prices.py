from src.db import db
from sqlalchemy.dialects.postgresql import UUID


class Prices(db.Model):
    __tablename__ = 'prices'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    model_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    model = db.relationship('ServiceParams', foreign_keys=[model_id])
    service_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    service = db.relationship('ServiceParams', foreign_keys=[service_id])
    problem_id = db.Column(UUID, db.ForeignKey('service_params.id'))
    problem = db.relationship('ServiceParams', foreign_keys=[problem_id])
    price = db.Column(db.INTEGER)
    price2 = db.Column(db.INTEGER)
    deprecated = db.Column(db.BOOLEAN, default=False, server_default=db.text('False'))
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    update_at = db.Column(db.TIMESTAMP(timezone=True),
                          server_default=db.text('now()::timestamp(0)'))

    @property
    def ger_prices_dict(self):
        return {
            'counted_price': self.price,
            'price': self.price,
            'price2': self.price2,
        }

    @property
    def model_pretty_info(self):
        return {
            'model': ['Модель', self.model.name]
        }
