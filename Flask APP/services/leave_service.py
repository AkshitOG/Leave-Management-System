from database.db_helper import *
from models.leave_request import LeaveRequest
from datetime import date 

class LeaveService:

    @staticmethod
    def createleave(leaverequestobject:LeaveRequest):
        query = """INSERT INTO LeaveRequests (EMPLOYEEID, LEAVETYPE, STARTDATE, ENDDATE, REASON)
        VALUES (?,?, ?, ?, ?)"""

        rows = execute_query(query,
                      [leaverequestobject.employeeid,
                        leaverequestobject.leavetype,
                        leaverequestobject.startdate,
                        leaverequestobject.enddate,
                        leaverequestobject.reason]
                    )
        
        return rows > 0
    
    @staticmethod
    def get_leaves_by_employee_id(employee_id:int):
        query = """SELECT *
        FROM LeaveRequests
        WHERE EMPLOYEEID = ?"""

        leaves_rows = fetchall(query, employee_id)

        return [LeaveRequest.from_row(row) for row in leaves_rows]
    
    @staticmethod
    def leave_details(request_id:int):
        query = """SELECT *
        FROM LeaveRequests
        WHERE REQUESTID = ?"""

        Leave_request = fetchone(query,request_id)
        if Leave_request is None:
            return None

        return LeaveRequest.from_row(Leave_request)
    
    @staticmethod
    def cancel_leave(request_id:int):
        leave = LeaveService.leave_details(request_id=request_id)
        if leave.can_cancel():
            query = """UPDATE LeaveRequests
            SET STATUS = ?
            WHERE REQUESTID = ?"""

            execute_query(query, ["CANCELLED", request_id])
            return True
        
        return False
    
    @staticmethod
    def get_pending(limit:int | None = None):
        if limit is not None:
            query = """SELECT TOP(?) *
            FROM LeaveRequests
            WHERE STATUS = ?
            ORDER BY CREATIONDATE DESC
            """
            pending_leaves_rows = fetchall(query, limit, "PENDING")
        else:
            query = """SELECT *
            FROM LeaveRequests
            WHERE STATUS = ?
            ORDER BY CREATIONDATE DESC
            """
            pending_leaves_rows = fetchall(query, "PENDING")

        return [LeaveRequest.from_row(pending_leave_req) for pending_leave_req in pending_leaves_rows]
    
    @staticmethod
    def approve_leave(request_id:int, employee_id:int, approved_by:int, comments:str, ):
        leave = LeaveService.leave_details(request_id)
        if leave.status != "Pending":
            return False
        
        queries = ["""UPDATE LeaveRequests
        SET STATUS = 'APPROVED'
        WHERE REQUESTID = ?""",

        """UPDATE Employees
        SET LEAVES_BALANCE = LEAVES_BALANCE - ?
        WHERE EMPLOYEEID = ?""",
        
        """INSERT INTO Approvals
        (REQUESTID,
        APPROVEDBY,
        DECISION,
        COMMENTS,
        APPROVALDATE)
        VALUES (?,?,'Approved',?,?)"""]

        dates = fetchone("""SELECT STARTDATE, ENDDATE
                              FROM LeaveRequests
                              WHERE REQUESTID = ?""", request_id)
        if dates is None:
            return False
        
        start_date = dates.STARTDATE
        end_date = dates.ENDDATE
        total_days = (end_date - start_date).days + 1

        execute_query(queries[0], request_id)
        execute_query(queries[1], [total_days, employee_id])
        execute_query(queries[2], [request_id, approved_by, comments, date.today()])
        return True

    @staticmethod
    def reject_leave(request_id:int, approved_by:int, comments:str):
        leave = LeaveService.leave_details(request_id)
        if leave.status != "Pending":
            return False
        
        queries = ["""UPDATE LeaveRequests
        SET STATUS = 'REJECTED'
        WHERE REQUESTID = ?""",
        
        """INSERT INTO Approvals
        (REQUESTID,
        APPROVEDBY,
        DECISION,
        COMMENTS,
        APPROVALDATE)
        VALUES (?,?,'Rejected',?,?)"""]

        execute_query(queries[0], request_id)
        execute_query(queries[1], [request_id, approved_by, comments, date.today()])
        return True
    
    