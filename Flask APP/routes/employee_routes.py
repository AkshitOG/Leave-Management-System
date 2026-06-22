from flask import Blueprint, session, request, redirect, url_for, render_template
from decorators.login_required import login_required
from services.dashboard_service import DashboardService

emp_bp = Blueprint(
    "employee",
    __name__
)

@login_required
@emp_bp.route("/dashboard")
def dashboard():
    
    stats = DashboardService.get_leave_stats(session.get("employee_id"))
    return render_template("employee_dashboarddashboard.html")