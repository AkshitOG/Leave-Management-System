from flask import Blueprint, render_template, request, redirect, url_for, flash
from decorators.login_required import login_required
from decorators.role_required import role_req
from services.admin_service import AdminService

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/dashboard")
@login_required
@role_req("ADMIN")
def dashboard():

    stats = AdminService.get_dashboard_stats()

    return render_template(
        "admin/admin_dashboard.html",
        stats=stats
    )


@admin_bp.route("/employees")
@login_required
@role_req("ADMIN")
def employees():

    employees = AdminService.get_all_employees()

    return render_template(
        "admin/employees.html",
        employees=employees
    )



@admin_bp.route("/create-employee", methods=["GET", "POST"])
@login_required
@role_req("ADMIN")
def create_employee():

    if request.method == "POST":

        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role": request.form.get("role"),
            "leave_balance": int(request.form.get("leave_balance"))
        }

        result = AdminService.create_employee(data)

        if result["success"]:
            flash("Employee created successfully", "success")
            return redirect(url_for("admin.employees"))

        flash(result["message"], "danger")

    return render_template("admin/create_employee.html")


@admin_bp.route("/balances")
@login_required
@role_req("ADMIN")
def balances():

    employees = AdminService.get_all_employees()

    return render_template(
        "admin/balances.html",
        employees=employees
    )