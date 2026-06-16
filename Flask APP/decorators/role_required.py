from functools import wraps
from flask import session, url_for, redirect, request

def role_req(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = session.get("role")
            if role is None:
                return redirect(url_for("auth.login", next = request.url))
            if role not  in roles:
                return redirect(url_for("auth.unauthorized"))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator