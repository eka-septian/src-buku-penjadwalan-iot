from flask import blueprints

bp = blueprints.Blueprint(
    "schedules", __name__, url_prefix="/schedules", template_folder="templates"
)

from . import routes
