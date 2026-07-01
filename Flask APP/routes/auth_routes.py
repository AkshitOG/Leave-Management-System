from flask import Blueprint, request, session, render_template, url_for, redirect, flash
from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        employee = AuthService.login(email=email, password=password)

        if employee is None:
            flash("Invalid Credentials", "danger")
            return render_template("login.html")

        session["employee_id"] = employee.EmployeeID
        session["name"] = employee.Name
        session["role"] = employee.Role
        session["email"] = employee.Email
        
        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)
        
        flash("Login Successful", "success")

        role = employee.Role.upper()

        if role == "ADMIN":
            return redirect(url_for("admin.dashboard"))

        elif role == "HR":
            return redirect(url_for("hr.dashboard"))

        else:
            return redirect(url_for("employee.dashboard"))

    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    session.clear()

    flash(
        "Logged Out Successfully",
        "info"
    )
    return redirect(url_for("auth.login"))

