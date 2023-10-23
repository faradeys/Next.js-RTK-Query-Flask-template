from webargs import fields

me_patch = {
    'name': fields.Str(),
    'city': fields.Str(),
    'avatar_id': fields.Str(),
}

me_phone_update_post = {
    'phone': fields.Str(),
    'verify_code': fields.Str()
}

me_mail_update_post = {
    'email': fields.Email(),
    'verify_code': fields.Str()
}

me_pass_update_post = {
    'old_pass': fields.Str(required=True),
    'new_pass': fields.Str(required=True)
}