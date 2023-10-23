import json
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import session, db
from src.db.models import UserServiceState
from src.lib.access import allow, validate_uuid
from src.schemas.user_service_state import user_service_state_post


class UserServiceStateAPI(Resource):
    @allow(['user'])
    def get(self, state_id=None):
        if not validate_uuid(state_id):
            return {
               "message": "Not found service state",
            }, 404

        state = UserServiceState.query.get(str(state_id))
        if not state:
            return {
                "message": "Not found service state"
            }, 404

        return {
            "saved_state": state.json_data
        }

    @allow(['user'])
    @use_args(user_service_state_post)
    def post(self, data):
        try:
            json_data = json.loads(data.get('json_data'))
        except ValueError:
            return {
                "message": "no such service type"
            }, 404

        state_id = UserServiceState.get_or_create(service_type_name=data.get('service_type'), json_data=json_data)
        if not state_id:
            return {
                "message": "no such service type"
            }, 404

        return {
            "state_id": state_id
        }

