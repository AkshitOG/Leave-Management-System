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
        employeeid = request.form.get("employee_id")
        password = request.form.get("password")

        employee = AuthService.login(employeeid=employeeid, password=password)

        if employee is None:
            flash("Invalid Credentials", "danger")
            return render_template("login.html")

        session["employee_id"] = employee.EmployeeID
        session["name"] = employee.Name
        session["role"] = employee.Role
        
        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)
        
        flash("Login Successfull")
        return redirect("/")

    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    session.clear()

    flash(
        "Logged Out Successfully",
        "info"
    )
    return redirect(url_for("auth.login"))

