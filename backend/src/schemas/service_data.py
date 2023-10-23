from webargs import fields, validate

service_phone_repair_post = {
    'type': fields.Str(required=True),
    'model': fields.Str(required=True),
    'defect_type': fields.Str(required=True)
}

service_phone_repair_orders_post = {
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'color': fields.Str(required=True),
    'model': fields.Str(required=True),
    'defect_type': fields.Str(required=True),
    'price_type': fields.Str(required=True),
    'sale': fields.Bool(default=False),
    'city': fields.Str(default=False),
    'meet_time': fields.Str(),
    'when_time': fields.Str(),
    'glass': fields.Str(default=False)
}
service_glass_post = {
    'color': fields.Str(required=True),
    'model': fields.Str(required=True),
    'type': fields.Str(required=True)
}

service_glass_orders_post = {
    'city': fields.Str(required=True),
    'color': fields.Str(required=True),
    'device_type': fields.Str(required=True),
    'meet_time': fields.Str(),
    'when_time': fields.Str(),
    'model': fields.Str(required=True),
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'price_type': fields.Str(required=True),

}