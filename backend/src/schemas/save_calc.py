from webargs import fields

save_calc_data = {
    'phone':fields.Str(required=True),
    'type': fields.Str(),
    'data': fields.Str(),
}