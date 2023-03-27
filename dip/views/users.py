from flask import Blueprint, make_response, render_template, request, url_for, current_app, redirect

from dip.utils.session import set_user_identity, authed_only, get_current_user, role_required
from dip.utils.security import remove_image_metadata, generate_password_hash
from dip.extensions import db

bp = Blueprint('bp_user', __name__)


bp.after_app_request(set_user_identity)


@bp.route('/profile', methods=['GET', 'POST'])
@authed_only
def profile():

    if request.method == 'GET':

        current_user = get_current_user()
        user_json = current_user.json()

        if user_json.get('photo'):
            user_json['photo'] = url_for(
                'static.send_user_image', id_=current_user.id)

        else:
            user_json['photo'] = url_for(
                'static', filename='img/profile-picture.jpg')

        return render_template('profile.html', user=user_json)

    else:
        current_user = get_current_user()
        user_json = current_user.json()

        user_data = request.form

        photo_file = request.files.get('photo')

        if photo_file.filename:
            filepath = current_app.config['PATHS']['user_images'] / \
                photo_file.filename

            if not filepath.exists():
                photo_file.save(filepath)
                remove_image_metadata(photo_file.filename)

            current_user.photo = photo_file.filename

        if user_data.get('password'):
            current_user.password = generate_password_hash(user_data.get(
                'password'), current_app.config['PASSWORD_SALT'])

        db.session.commit()

        return redirect(url_for('bp_user.profile'))

@bp.route('/profile/<id_>', methods=['GET', 'POST'])
@role_required(['user', 'admin'])
def profile_id(id_):
    print("OK")
    # if request.method == 'GET':
    #
    #     current_user = get_current_user()
    #     user_json = current_user.json()
    #
    #     if user_json.get('photo'):
    #         user_json['photo'] = url_for(
    #             'static.send_user_image', id_=current_user.id)
    #
    #     else:
    #         user_json['photo'] = url_for(
    #             'static', filename='img/profile-picture.jpg')
    #
    #     return render_template('profile.html', user=user_json)
