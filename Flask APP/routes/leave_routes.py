from flask import Blueprint

leave_bp = Blueprint(
    "leave",
    __name__
)

@leave_bp.route("/")
def leavepage():
    return "Leave Page"
