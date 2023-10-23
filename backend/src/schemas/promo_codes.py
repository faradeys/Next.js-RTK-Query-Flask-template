from webargs import fields

check_promo_code_post = {
    'promo_code': fields.Str(required=True),
    'device_type': fields.Str(required=True),
    'order_type': fields.Str(required=True),
    'price': fields.Integer(required=True)
}