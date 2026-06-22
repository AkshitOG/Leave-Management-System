from flask import Blueprint, request, flash, redirect, url_for, session, render_template
from services.leave_service import LeaveService
from decorators.login_required import login_required
from models.leave_request import LeaveRequest

leave_bp = Blueprint(
    "leave",
    __name__,
    url_prefix="/leaves"
)

@login_required
@leave_bp.route("/new", methods=["GET", "POST"])
def leavepage():
    if request.method == "POST":
        employee_id = session.get("employee_id")
        leavetype = request.form.get("leave_type")
        startdate = request.form.get("start_date")
        enddate = request.form.get("end_date")
        reason = request.form.get("reason")

        leavereq = LeaveRequest(empid=employee_id, leave_type=leavetype, startdate=startdate, enddate=enddate, reason=reason)
        leave = LeaveService.createleave(leavereq)

        if leave is None or leave == False:
            flash("Failed to Create Leave", "danger")
            return redirect(url_for("leave.leavepage"))
        
        flash("Leave Saved Successfully", "success")
        return redirect(url_for("employee.dashboard"))

    return render_template("leaves_page.html")

@login_required
@leave_bp.route("/", methods=["GET"])
def history_page():
    employee_id = session.get("employee_id")

    leaves = LeaveService.get_leaves_by_employee_id(employee_id=employee_id)

    return render_template("leave_history.html", leaves=leaves)

@login_required
@leave_bp.route("/<int:request_id>")
def request_details(request_id:int):
    current_employee_id = session.get("employee_id")
    leave = LeaveService.leave_details(request_id=request_id)
    if leave is None:
        return redirect("/")
    if leave.employee_id != current_employee_id:
        return redirect("/")
    
    return render_template("request_details.html", leave_details=leave)

@login_required
@leave_bp.route("/<int:request_id>/cancel", methods=["GET","POST"])
def cancel_leave(request_id:int):
    leave = LeaveService.leave_details(request_id=request_id)
    current_employee_id = session.get("employee_id")
    if leave is None:
        return redirect("/")
    if leave.employee_id != current_employee_id:
        return redirect("/")
    
    if request.method == "POST":
        _ = LeaveService.cancel_leave(request_id=request_id)
        if _ == False:
            flash("Failed to Cancel this leave","danger")
        else:
            flash("Cancelled Successfully", "success")
            return redirect(url_for("leave.request_details", request_id = request_id))
        
    return render_template("cancellation.html")