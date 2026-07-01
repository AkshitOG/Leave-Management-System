from datetime import date

class LeaveRequest:
    request_id:int
    employee_id:int
    leave_type:str
    start_date:date
    end_date:date
    reason:str
    status:str
    creation_date:date

    def __init__(self, empid:int, leave_type:str, startdate:date, enddate:date, reason:str, reqid:int|None = None, status:str | None = None, createdate:date | None = None):
        self.request_id = reqid
        self.employee_id = empid
        self.leave_type = leave_type
        self.start_date = startdate
        self.end_date = enddate
        self.reason = reason
        self.status = status if status is not None else "PENDING"
        self.creation_date = createdate if createdate is not None else date.today()

    @classmethod
    def from_row(cls, row):
        return cls(
            reqid=row.REQUESTID,
            empid=row.EMPLOYEEID,
            leave_type=row.LEAVETYPE,
            startdate=row.STARTDATE,
            enddate=row.ENDDATE,
            reason=row.REASON,
            status=row.STATUS,
            createdate=row.CREATIONDATE
            )

    def is_pending(self):
        return self.status == "Pending"
    
    def can_cancel(self):
        return self.is_pending()
    
    def total_days(self):
        return (self.end_date - self.start_date).days + 1