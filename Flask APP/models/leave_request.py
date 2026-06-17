from datetime import date

class LeaveRequest:
    requestid:int
    employeeid:int
    leavetype:str
    startdate:date
    enddate:date
    reason:str
    status:str
    creationdate:date

    def __init__(self, reqid:int, empid:int, leave_type:str, startdate:date, enddate:date, reason:str, status:str, createdate:date):
        self.requestid = reqid
        self.employeeid = empid
        self.leavetype = leave_type
        self.startdate = startdate
        self.enddate = enddate
        self.reason = reason
        self.status = status
        self.creationdate = createdate
