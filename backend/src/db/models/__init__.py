"""models init."""
import inspect
from flask_sqlalchemy import Model

from .role import Role
from .file import File
from .service_params import ServiceParams
from .prices import Prices
from .orders import Orders
from .user_service_state import UserServiceState
from .referal_codes import ReferalCode
from .user_text_store import UserTextStore
from .promo_codes import PromoCodes
from .promo_codes_orders import PromoCodesOrders

from .many_to_many import (
    users_roles,
    roles_parents,
)
from .user import User

ALL_MODELS = {x.__name__: x for x in locals().values()
              if inspect.isclass(x) and
              issubclass(x, Model) and
              x != Model}
