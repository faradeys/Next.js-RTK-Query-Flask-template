from webargs import fields

login_post = {
    'phone': fields.Str(required=True),
    'password': fields.Str(required=True)
}

reg_post = {
    'phone': fields.Str(required=True),
    'name': fields.Str(),
    'password': fields.Str()
}

restore_pass_post = {
    'phone': fields.Str(required=True),
    'token': fields.Str(required=True)
}

vk_side_auth_post = {
    'access_token': fields.Str(required=True)
}

fb_side_auth_post = {
    'access_token': fields.Str(required=True)
}
