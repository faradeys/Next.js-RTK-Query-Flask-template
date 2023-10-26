"""models init."""
import inspect
from flask_sqlalchemy import Model

from .role import Role
from .file import File
from .service_params import ServiceParams

from .many_to_many import (
    users_roles,
    roles_parents,
)
from .user import User

ALL_MODELS = {x.__name__: x for x in locals().values()
              if inspect.isclass(x) and
              issubclass(x, Model) and
              x != Model}
