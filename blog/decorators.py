from flask import session, request, redirect

from functools import wraps

def auth_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['authenticated']:
                return f(*args, **kwargs)                        
            else:
                path = request.path
                return redirect('/login?redirect=' + path)
        except KeyError:
            return redirect('/login?redirect=' + request.path)

    return decorated_function