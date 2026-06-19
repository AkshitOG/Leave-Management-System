from database.db_helper import *
from models.leave_request import LeaveRequest

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