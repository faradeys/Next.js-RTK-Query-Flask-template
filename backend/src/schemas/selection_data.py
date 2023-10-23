from webargs import fields, validate

selection_data_post = {
    "device_type": fields.Str(),
    "model": fields.Str(),
    "memory": fields.Str(),
    "mount": fields.Str(),
    "type": fields.Str(),
    "phone": fields.Str(),
    "comment": fields.Str(),
    "person_name": fields.Str()
}