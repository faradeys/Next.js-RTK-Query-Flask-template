from webargs import fields

check_referal_code_post = {
    'referal_code': fields.Str(required=True)
}

invite_friend_post = {
    'phone': fields.Str(required=True),
    'referal_code': fields.Str(required=True)
}