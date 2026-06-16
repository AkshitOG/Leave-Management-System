from flask import session, redirect, url_for, request
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        employee_id = session.get("employee_id")

        if employee_id is None:
            return redirect(url_for("auth.login", next = request.url))
        return func(*args, **kwargs)
    return wrapper
