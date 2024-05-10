from flask import blueprints

bp = blueprints.Blueprint(
    "auth", __name__, url_prefix="/auth", template_folder="templates"
)

from . import routes
