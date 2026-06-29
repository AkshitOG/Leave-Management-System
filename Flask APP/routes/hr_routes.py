from flask import Blueprint, render_template, session
from decorators.login_required import login_required
from decorators.role_required import role_req
from services.leave_service import LeaveService
from services.dashboard_service import DashboardService

hr_bp = Blueprint(
    "hr",
    __name__,
)

@hr_bp.route("/dashboard")
@login_required
@role_req("HR")
def dashboard():
    pending_leaves:list = LeaveService.get_pending(limit=5)
    stats = DashboardService.get_leave_stats(session.get("employee_id"))
    return render_template("hr_dashboard.html",pending_leaves=pending_leaves, stats=stats)

@hr_bp.route("/all-pending-leaves")
@login_required
@role_req("HR", "ADMIN")
def all_pending_leaves():
    pending_leaves = LeaveService.get_pending()
    return render_template("leave-page.html", pending_leaves=pending_leaves)