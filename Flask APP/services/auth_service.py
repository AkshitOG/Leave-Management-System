from database.db_helper import *
from models.employee import Employee
from werkzeug.security import check_password_hash

class AuthService:

    @staticmethod
    def get_user_by_id(empid):
        query = """SELECT *
        FROM Employees
        WHERE EMPLOYEEID = ?"""

        row = fetchone(query, empid)
        
        if row is None:
            return None
        
        return Employee(
            row.EMPLOYEEID,
            row.NAME,
            row.EMAIL,
            row.PASSWORDHASH,
            row.ROLE,
            row.JOINDATE,
            row.LEAVES_BALANCE
        )
    
    @staticmethod
    def login(employeeid:int, password:str):

        employee = AuthService.get_user_by_id(empid=employeeid)

        if employee is None:
            return None
        
        if not check_password_hash(employee.Password_hash, password):
            return None
        
        return employee