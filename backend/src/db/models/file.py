import os
import hashlib
from flask import g
from src.db import db, session
from sqlalchemy.dialects.postgresql import UUID
from PIL import Image as ImgEdit
from pathlib import Path
from simple_storage import FileStorage
from io import BytesIO

from utils import get_config


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(UUID,
                server_default=db.text('gen_random_uuid()'),
                primary_key=True)

    filename = db.Column(db.VARCHAR(50)) #better cutoff filename length from neccessary data
    ext = db.Column(db.VARCHAR(8))
    file_mimetype = db.Column(db.VARCHAR(35))
    size = db.Column(db.INTEGER)
    md5hash = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.text('now()'))
    created_by = db.Column(UUID, db.ForeignKey('users.id'))


    @classmethod
    def store(cls, created_by, fullname, binary, mimetype=None, as_avatar=False):
        size = len(binary)
        filename, ext = os.path.splitext(fullname)
        ext = ext.replace('.', '') if ext else None
        storage = FileStorage(get_config('UPLOAD_DIR'), max_filesize=get_config('MAX_AVATAR_CONTENT_LENGTH'))

        if as_avatar:
            binary = cls.make_avatar(binary)
            size = len(binary)
            mimetype = 'image/jpeg'
            ext = 'jpg'
        try:
            md5hash = storage.store_file(ext, binary)
        except FileExistsError:
            md5hash = hashlib.md5(binary).hexdigest()

        _file = session \
            .query(cls) \
            .filter_by(md5hash=md5hash).first()

        if not _file:
            _file = cls(
                filename=filename[:50],
                ext=ext,
                file_mimetype=mimetype,
                size=size,
                md5hash=md5hash,
                created_by=created_by
            )
            session.add(_file)
            session.commit()
        return _file


    @staticmethod
    def make_avatar(binary):
        """make avatar"""

        img = ImgEdit.open(BytesIO(binary))
        img = img.convert("RGB")

        width, height = img.size
        left = upper = 0
        right = width
        lower = height
        if width > height:
            left = (width - height) / 2
            right = width - ((width - height) / 2)
        if height > width:
            upper = (height - width) / 2
            lower = height - ((height - width) / 2)

        cropped_img = img.crop((left, upper, right, lower))
        resized_img = cropped_img.resize((get_config('AVATAR_SQUARE_SIDE_SIZE'), get_config('AVATAR_SQUARE_SIDE_SIZE')), ImgEdit.LANCZOS)
        resized_img_binary = BytesIO()
        resized_img.save(resized_img_binary, 'JPEG')
        return resized_img_binary.getvalue()


    def public_path(self):
        storage = FileStorage(get_config('UPLOAD_DIR'))
        public_root = Path(get_config('PUBLIC_ROOT'))
        try:
            local_path = Path(storage.get_file_path(self.md5hash))
        except FileNotFoundError:
            return None
        return '/' + str(local_path.relative_to(public_root))


    def absolute_path(self):
        pp = self.public_path()
        if pp:
            return get_config('SITE_URL') + pp
        return None
