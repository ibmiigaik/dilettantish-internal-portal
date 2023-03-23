import base64
import functools
import json

from flask import current_app, request, redirect, url_for, g

from dip.models import User
from dip.utils.security import is_valid_signature, create_signature

AUTHED_ROLES = [
    'user',
    'admin'
]


SESSION_COOKIE_NAME = 'session_cookie'



# anonymous identity if not exists
def set_user_identity(response):

    if request.cookies.get(SESSION_COOKIE_NAME):
        return response

    if not response.headers.get('Set-Cookie', '') or SESSION_COOKIE_NAME not in response.headers.get('Set-Cookie', ''):
            response.set_cookie(
                SESSION_COOKIE_NAME,
                create_session()
                )
    
    
    return response


def get_current_user():
    if not request.cookies.get(SESSION_COOKIE_NAME):
        return None

    identity_json = base64.b64decode(request.cookies.get(SESSION_COOKIE_NAME))
    identity = json.loads(identity_json)

    if not is_valid_signature(identity, current_app.config['SECRET_KEY']):
        return None

    user = User.query.filter_by(username=identity['username']).first()

    return user


# Здесь нужно просто хранилище проверить
# посмотреть, как работает JWT
def authed_only(f):
    @functools.wraps(f)
    def authed_only_wrapper(*args, **kwargs):
        if authed():
            g.user = get_current_user()
            return f(*args, **kwargs)
        else:
            return redirect(url_for('bp_auth.login'))   

    return authed_only_wrapper


def admin_only(f):
    @functools.wraps(f)
    def admin_only_wrapper(*args, **kwargs):
        if authed():
            user = get_current_user()
            g.user = user
            if user.role == 'admin':
                return f(*args, **kwargs)

        else:
            return render_template('errors/403.html'), 403

    return admin_only_wrapper



def authed():
    if not request.cookies.get(SESSION_COOKIE_NAME):
        return False

    identity_json = base64.b64decode(request.cookies.get(SESSION_COOKIE_NAME))
    identity = json.loads(identity_json)

    if not is_valid_signature(identity, current_app.config['SECRET_KEY']):
        return False

    user = User.query.filter_by(username=identity['username']).first()

    if user:
        return True



def is_valid_role(request):
    if not request.cookies.get(SESSION_COOKIE_NAME):
        return False

    identity = base64.b64decode(request.cookies.get(SESSION_COOKIE_NAME))

    if identity.get('role') in AUTHED_ROLES:
        return True


def create_session(username='anonymous', role='anonymous'):
    signature = create_signature(username, role, current_app.config['SECRET_KEY'])

    identity = {
        'username': username,
        'role': role,
        'signature': signature
    }

    identity_json = json.dumps(identity)

    identity_b64 = base64.b64encode(identity_json.encode())

    return identity_b64
