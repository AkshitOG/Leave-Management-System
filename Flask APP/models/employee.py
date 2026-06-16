from datetime import date

class Employee:
    EmployeeID:int | None
    Name:str
    Email:str
    Password_hash:str
    Role:str
    JoinDate: date
    Leaves_Balance:int
    
    def __init__(self, empid, name, email, hashedpassword, role, joindate, leaves_bal):
        self.EmployeeID = empid
        self.Name = name
        self.Email = email
        self.Password_hash = hashedpassword
        self.Role = role
        self.JoinDate = joindate
        self.Leaves_Balance = leaves_bal
    
    
