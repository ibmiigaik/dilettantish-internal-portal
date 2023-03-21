from flask import Blueprint


bp = Blueprint('static', __name__)


@bp.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)