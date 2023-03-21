from flask import Blueprint, make_response, render_template, request, url_for

from dip.utils.session import set_user_identity, authed_only

bp = Blueprint('bp_user', __name__)


bp.after_app_request(set_user_identity)


@bp.route('/profile', methods=['GET'])
@authed_only
def profile():

    return render_template('profile.html')


@bp.route('/profile/:id', methods=['GET'])
@role_required(['admin', 'user'])
def user_profile():
    pass

