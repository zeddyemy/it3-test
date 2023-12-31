from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.routes.api import auth, payment, items, item_interactions, location, task, task_performance, profile, referral