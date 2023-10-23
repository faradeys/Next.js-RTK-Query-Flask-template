from webargs import fields

get_users_texts = {
    'phone': fields.Str(required=True)
}

set_user_text_post = {
    'title': fields.Str(),
    'name': fields.Str(),
    'email': fields.Str(),
    'phone': fields.Str(),
    'text': fields.Str(),
    'utm': fields.Str(),
    'token': fields.Str(),
    'from': fields.Str(),
}