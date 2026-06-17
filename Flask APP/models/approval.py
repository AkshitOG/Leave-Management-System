from employee import Employee
from leave_request import LeaveRequest
from datetime import date

class Approval:
    requestid:int
    ApprovalID:int
    RequestedBy:Employee
    ApprovedBy:Employee
    Decision:str
    Comments:str
    ApprovalDate:date

    def __init__(self, approvalid:int, requestby:Employee, approveby:Employee, decision:str, comment:str, approvedate:date):
        self.ApprovalID = approvalid
        self.RequestedBy = requestby
        self.ApprovedBy = approveby
        self.Decision = decision
        self.Comments = comment
        self.ApprovalDate = approvedate
        
    