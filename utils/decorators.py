from functools import wraps
from flask import session, redirect, url_for, abort

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('auth.connexion'))
            if role and session.get('role') != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator