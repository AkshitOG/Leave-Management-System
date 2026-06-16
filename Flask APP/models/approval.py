from employee import Employee
from datetime import date

class Approval:
    ApprovalID:int
    RequestedBy:Employee
    ApprovedBy:Employee
    Decision:str
    Comments:str
    ApprovalDate:date

    def __init__(self, approvalid, requestby, approveby, decision, comment, approvedate):
        self.ApprovalID = approvalid
        self.RequestedBy = requestby
        self.ApprovedBy = approveby
        self.Decision = decision
        self.Comments = comment
        self.ApprovalDate = approvedate
        
    