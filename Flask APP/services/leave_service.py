from datetime import date

from database.db_helper import *
from models.leave_request import LeaveRequest
from services.email_service import EmailService


class LeaveService:

    @staticmethod
    def createleave(leaverequestobject: LeaveRequest):
        query = """
        INSERT INTO LeaveRequests
        (EMPLOYEEID, LEAVETYPE, STARTDATE, ENDDATE, REASON)
        VALUES (?, ?, ?, ?, ?)
        """

        rows = execute_query(
            query,
            [
                leaverequestobject.employee_id,
                leaverequestobject.leave_type,
                leaverequestobject.start_date,
                leaverequestobject.end_date,
                leaverequestobject.reason,
            ],
        )

        return rows > 0

    @staticmethod
    def get_leaves_by_employee_id(employee_id: int):
        query = """
        SELECT *
        FROM LeaveRequests
        WHERE EMPLOYEEID = ?
        ORDER BY CREATIONDATE DESC
        """

        rows = fetchall(query, employee_id)

        return [LeaveRequest.from_row(row) for row in rows]

    @staticmethod
    def leave_details(request_id: int):
        query = """
        SELECT *
        FROM LeaveRequests
        WHERE REQUESTID = ?
        """

        row = fetchone(query, request_id)

        if row is None:
            return None

        return LeaveRequest.from_row(row)

    @staticmethod
    def cancel_leave(request_id: int):

        leave = LeaveService.leave_details(request_id)

        if leave is None:
            return False

        if not leave.can_cancel():
            return False

        execute_query(
            """
            UPDATE LeaveRequests
            SET STATUS='CANCELLED'
            WHERE REQUESTID=?
            """,
            request_id,
        )

        return True

    @staticmethod
    def get_pending(limit=None):

        if limit is not None:

            query = """
            SELECT TOP(?)
            *
            FROM LeaveRequests
            WHERE STATUS='PENDING'
            ORDER BY CREATIONDATE DESC
            """

            rows = fetchall(query, [limit])

        else:

            query = """
            SELECT *
            FROM LeaveRequests
            WHERE STATUS='PENDING'
            ORDER BY CREATIONDATE DESC
            """

            rows = fetchall(query)

        return [LeaveRequest.from_row(row) for row in rows]

    @staticmethod
    def approve_leave(request_id: int, hr_id: int):

        leave = LeaveService.leave_details(request_id)

        if leave is None:
            return False

        if leave.status.strip().upper() != "PENDING":
            return False

        employee = fetchone(
            """
            SELECT EMAIL, LEAVES_BALANCE
            FROM Employees
            WHERE EMPLOYEEID = ?
            """,
            leave.employee_id,
        )

        if employee is None:
            return False

        leave_days = (leave.end_date - leave.start_date).days + 1

        if employee.LEAVES_BALANCE < leave_days:
            return False

        execute_query(
            """
            UPDATE LeaveRequests
            SET STATUS='APPROVED'
            WHERE REQUESTID=?
            """,
            request_id,
        )

        execute_query(
            """
            UPDATE Employees
            SET LEAVES_BALANCE = LEAVES_BALANCE - ?
            WHERE EMPLOYEEID = ?
            """,
            [leave_days, leave.employee_id],
        )

        execute_query(
            """
            INSERT INTO Approvals
            (
                REQUESTID,
                APPROVEDBY,
                DECISION,
                COMMENTS,
                APPROVALDATE
            )
            VALUES (?, ?, ?, ?, GETDATE())
            """,
            [
                request_id,
                hr_id,
                "APPROVED",
                "Approved by HR",
            ],
        )

        try:
            EmailService.send_approve_mail(
                employee.EMAIL,
                request_id,
            )
        except Exception as e:
            print("Mail Error:", e)

        return True

    @staticmethod
    def reject_leave(request_id: int, hr_id: int):

        leave = LeaveService.leave_details(request_id)

        if leave is None:
            return False

        if leave.status.strip().upper() != "PENDING":
            return False

        employee = fetchone(
            """
            SELECT EMAIL
            FROM Employees
            WHERE EMPLOYEEID = ?
            """,
            leave.employee_id,
        )

        if employee is None:
            return False

        execute_query(
            """
            UPDATE LeaveRequests
            SET STATUS='REJECTED'
            WHERE REQUESTID=?
            """,
            request_id,
        )

        execute_query(
            """
            INSERT INTO Approvals
            (
                REQUESTID,
                APPROVEDBY,
                DECISION,
                COMMENTS,
                APPROVALDATE
            )
            VALUES (?, ?, ?, ?, GETDATE())
            """,
            [
                request_id,
                hr_id,
                "REJECTED",
                "Rejected by HR",
            ],
        )

        try:
            EmailService.send_reject_mail(
                employee.EMAIL,
                request_id,
            )
        except Exception as e:
            print("Mail Error:", e)

        return True