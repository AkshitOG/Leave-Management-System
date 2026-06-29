from flask import Blueprint, session, request, redirect, url_for, render_template
from decorators.login_required import login_required
from services.dashboard_service import DashboardService

emp_bp = Blueprint(
    "employee",
    __name__
)

@emp_bp.route("/dashboard")
@login_required
def dashboard():
    
    stats = DashboardService.get_leave_stats(session.get("employee_id"))
    return render_template("employee_dashboard.html", stats=stats)