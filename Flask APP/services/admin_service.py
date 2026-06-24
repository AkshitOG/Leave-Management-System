from database.db_helper import *

class AdminRepository:

    @staticmethod
    def count_Employees():
        query = "SELECT COUNT(*) as count FROM Employees"
        result = fetchone(query)
        return result["count"]

    @staticmethod
    def count_pending_leaves():
        query = "SELECT COUNT(*) as count FROM leaves WHERE status = 'pending'"
        result = fetchone(query)
        return result["count"]

    @staticmethod
    def count_approved_leaves():
        query = "SELECT COUNT(*) as count FROM leaves WHERE status = 'approved'"
        result = fetchone(query)
        return result["count"]

    @staticmethod
    def get_all_Employees():
        query = """
        SELECT id, name, EMPLOYEEID, department, role
        FROM Employees
        ORDER BY id DESC
        """
        return fetchall(query)

    

    @staticmethod
    def insert_employee(data):
        query = """
        INSERT INTO Employees (name, EMPLOYEEID, password, department, role)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        result = fetchone(query, (
            data["name"],
            data["EMPLOYEEID"],
            data["password"],
            data["department"],
            data["role"]
        ))

        return result["id"]

class AdminService:

    @staticmethod
    def get_dashboard_stats():
        """
        Returns admin overview data
        """
        total_Employees = AdminRepository.count_Employees()
        pending_leaves = AdminRepository.count_pending_leaves()
        approved_leaves = AdminRepository.count_approved_leaves()

        return {
            "total_Employees": total_Employees,
            "pending_leaves": pending_leaves,
            "approved_leaves": approved_leaves
        }

    @staticmethod
    def get_all_Employees():
        """
        Fetch all Employees
        """
        return AdminRepository.get_all_Employees()

    @staticmethod
    def create_employee(data):
        """
        Create a new employee
        """

        # basic validation
        if AdminRepository.EMPLOYEEID_exists(data["EMPLOYEEID"]):
            return {"success": False, "message": "EMPLOYEEID already exists"}

        # password handling (assume utility exists)
        hashed_password = PasswordUtils.hash(data["password"])

        employee_data = {
            "name": data["name"],
            "EMPLOYEEID": data["EMPLOYEEID"],
            "password": hashed_password,
            "department": data.get("department", "General"),
            "role": "employee"
        }

        emp_id = AdminRepository.insert_employee(employee_data)

        return {
            "success": True,
            "employee_id": emp_id
        }