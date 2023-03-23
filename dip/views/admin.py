from flask import Blueprint, make_response, render_template, request, url_for

from dip.utils.session import set_user_identity, admin_only

bp = Blueprint('bp_admin', __name__)


@bp.route('/admin/dashboard/users', methods=['GET'])
@admin_only
def users():
    return render_template('admin_dashboard_users.html')


@bp.route('/admin/dashboard/job-titles', methods=['GET'])
@admin_only
def job_titles():
    return render_template('admin_dashboard_job_titles.html')