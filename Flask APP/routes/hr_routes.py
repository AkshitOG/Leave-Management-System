from flask import Blueprint, render_template, session
from decorators.login_required import login_required
from decorators.role_required import role_req
from services.leave_service import LeaveService
from services.dashboard_service import DashboardService

hr_bp = Blueprint(
    "hr",
    __name__,
)

@login_required
@role_req("HR")
@hr_bp.route("/dashboard")
def dashboard():
    pending_leaves:list = LeaveService.get_pending("EMPLOYEES")
    stats = DashboardService.get_leave_stats(session.get("employee_id"))
    return render_template("hr_dashboard.html",pending_leaves=pending_leaves, stats=stats)