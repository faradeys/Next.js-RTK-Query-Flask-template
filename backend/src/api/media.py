from flask import request, g
from flask_restful import Resource
from webargs.flaskparser import use_args
from simple_storage import TooBigFileException

from src.db import session
from src.lib.utils import get_config
from src.db.models import File
from src.lib.access import allow, validate_uuid


class FileUploadAPI(Resource):
    def get(self, uid=None):
        if not validate_uuid(uid):
            return {
               "message": "No such file",
            }, 404

        file = session.query(File).get(uid)
        if not file:
            return {
                'message': 'No such file',
            }, 404
        return file.absolute_path()


    @allow(['user'])
    def post(self):
        as_avatar = False
        user_file = request.files.get("file")
        if not user_file:
            return {
               'message': 'No file provided'
            }, 400

        if request.form.get("as_avatar") == '1':
            if not user_file.mimetype[:6] == 'image/':
                return {
                    "message": "{} неверный mimetype для изображения типа".format(request.files['img'].mimetype),
                }, 400
            as_avatar = True

        try:
            file = File.store(
                created_by=g.current_user.id,
                fullname=user_file.filename,
                binary=user_file.stream.read(),
                mimetype=user_file.mimetype,
                as_avatar=as_avatar
            )
        except TooBigFileException:
            return {
                'message': 'Too big filesize'
            }, 400

        return {
            'id': file.id,
            'path': file.absolute_path()
        }, 200
