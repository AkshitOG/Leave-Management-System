from datetime import date

class Employee:
    EmployeeID:int | None
    Name:str
    Email:str
    Password_hash:str
    Role:str
    JoinDate: date
    Leaves_Balance:int
    
    def __init__(self, empid:int|None, name:str, email:str, hashedpassword:str, role:str, joindate:date, leaves_bal:int):
        self.EmployeeID = empid
        self.Name = name
        self.Email = email
        self.Password_hash = hashedpassword
        self.Role = role
        self.JoinDate = joindate
        self.Leaves_Balance = leaves_bal
    
    
