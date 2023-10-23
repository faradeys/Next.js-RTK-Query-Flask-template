import json

from src.db import db
from sqlalchemy.dialects.postgresql import UUID

class UserTextStore(db.Model):
    __tablename__ = 'user_text_store'

    id = db.Column(UUID,
                   server_default=db.text('gen_random_uuid()'),
                   primary_key=True)
    name = db.Column(db.VARCHAR(256))
    email = db.Column(db.VARCHAR(160))
    phone = db.Column(db.VARCHAR(50), index=True)
    text = db.Column(db.TEXT)
    utm = db.Column(db.TEXT)
    created_at = db.Column(db.TIMESTAMP(timezone=True),
                           server_default=db.text('now()::timestamp(0)'))
    custom = db.Column(db.TEXT)
    message_id = db.Column(db.VARCHAR(250))

    @property
    def custom_params(self):
        if self.custom:
            return json.loads(self.custom)
        else:
            return {}
    
    def custom_upd(self, dic):
        self.custom = json.dumps(dic)
        return True
