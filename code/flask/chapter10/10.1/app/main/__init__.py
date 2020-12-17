from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)


def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors
