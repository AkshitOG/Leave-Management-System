from database.db_helper import execute_query
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