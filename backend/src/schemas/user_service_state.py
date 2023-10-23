from webargs import fields, validate

user_service_state_post = {
    'service_type': fields.Str(required=True,validate=validate.OneOf(choices=['iphone_tradein','macbook_tradein','samsung_tradein']),error='Non existed service type. Available: {choices}'),
    'json_data': fields.Str(required=True)
}