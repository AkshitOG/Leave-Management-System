from flask import Blueprint, request, flash, redirect, url_for, session, render_template
from services.leave_service import LeaveService
from decorators.login_required import login_required
from models.leave_request import LeaveRequest

leave_bp = Blueprint(
    "leave",
    __name__,
    url_prefix="/leave"
)

@login_required
@leave_bp.route("/", methods=["GET", "POST"])
def leavepage():
    if request.method == "POST":
        employee_id = session.get("employee_id")
        leavetype = request.form.get("leave_type")
        startdate = request.form.get("start_date")
        enddate = request.form.get("end_date")
        reason = request.form.get("reason")

        leavereq = LeaveRequest(empid=employee_id, leave_type=leavetype, startdate=startdate, enddate=enddate, reason=reason)
        leave = LeaveService.createleave(leavereq)

        if leave is None:
            flash("Failed to Create Leave", "danger")
            return redirect(url_for("leave.leavepage"))
        
        flash("Leave Saved Successfully", "success")
        return redirect(url_for("employee.dashboard"))

    return render_template("leaves_page.html")