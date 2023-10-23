from webargs import fields

bonuses_topup_post = {
    'phone': fields.Str(required=True),
    'value': fields.Integer(required=True)
}

bonuses_chargeoff_post = {
    'phone': fields.Str(required=True),
    'value': fields.Integer(required=True)
}