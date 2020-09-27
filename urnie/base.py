from flask import redirect, url_for, Blueprint


base_bp = Blueprint('base_bp', __name__)


@base_bp.route('/')
def base():
    return redirect(url_for('urn_bp.home'))
