from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from decorators.login_required import login_required
from decorators.role_required import role_req

from services.leave_service import LeaveService
from services.dashboard_service import DashboardService

hr_bp = Blueprint(
    "hr",
    __name__,
    url_prefix="/hr"
)


@hr_bp.route("/dashboard")
@login_required
@role_req("HR")
def dashboard():

    pending_leaves = LeaveService.get_pending(limit=5)
    stats = DashboardService.get_leave_stats(session.get("employee_id"))

    return render_template(
        "hr_dashboard.html",
        pending_leaves=pending_leaves,
        stats=stats
    )


@hr_bp.route("/all-pending-leaves")
@login_required
@role_req("HR")
def all_pending_leaves():

    pending_leaves = LeaveService.get_pending()

    return render_template(
        "leave-page.html",
        pending_leaves=pending_leaves
    )


@hr_bp.route("/leave/<int:request_id>")
@login_required
@role_req("HR")
def leave_details(request_id):

    leave = LeaveService.leave_details(request_id)

    if leave is None:
        flash("Leave request not found.", "danger")
        return redirect(url_for("hr.all_pending_leaves"))

    return render_template(
        "hr/request_details.html",
        leave=leave
    )


@hr_bp.route("/leave/<int:request_id>/approve", methods=["POST"])
@login_required
@role_req("HR")
def approve_leave(request_id):

    try:
        hr_id = session["employee_id"]

        result = LeaveService.approve_leave(request_id, hr_id)

        if result:
            flash("Leave approved successfully.", "success")
        else:
            flash("Unable to approve leave.", "danger")

    except Exception as e:
        print(e)
        flash(f"Error: {e}", "danger")

    return redirect(url_for("hr.all_pending_leaves"))


@hr_bp.route("/leave/<int:request_id>/reject", methods=["POST"])
@login_required
@role_req("HR")
def reject_leave(request_id):

    try:
        hr_id = session["employee_id"]

        result = LeaveService.reject_leave(request_id, hr_id)

        if result:
            flash("Leave rejected successfully.", "success")
        else:
            flash("Unable to reject leave.", "danger")

    except Exception as e:
        print(e)
        flash(f"Error: {e}", "danger")

    return redirect(url_for("hr.all_pending_leaves"))