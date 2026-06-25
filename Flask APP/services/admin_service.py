from datetime import date
from werkzeug.security import generate_password_hash
from database.db_helper import *


class AdminRepository:

    @staticmethod
    def count_employees():
        query = """
        SELECT COUNT(*) AS count
        FROM Employees
        """
        result = fetchone(query)
        return result.count

    @staticmethod
    def count_pending_leaves():
        query = """
        SELECT COUNT(*) AS count
        FROM LeaveRequests
        WHERE STATUS = 'PENDING'
        """
        result = fetchone(query)
        return result.count

    @staticmethod
    def count_approved_leaves():
        query = """
        SELECT COUNT(*) AS count
        FROM LeaveRequests
        WHERE STATUS = 'APPROVED'
        """
        result = fetchone(query)
        return result.count

    @staticmethod
    def get_all_employees():
        query = """
        SELECT
            EMPLOYEEID,
            NAME,
            EMAIL,
            ROLE,
            JOINDATE,
            LEAVES_BALANCE
        FROM Employees
        ORDER BY EMPLOYEEID DESC
        """
        return fetchall(query)

    @staticmethod
    def email_exists(email: str):
        query = """
        SELECT *
        FROM Employees
        WHERE EMAIL = ?
        """

        employee = fetchone(query, email)
        return employee is not None

    @staticmethod
    def insert_employee(
        name: str,
        email: str,
        password_hash: str,
        role: str,
        leave_balance: int
    ):
        query = """
        INSERT INTO Employees
        (
            NAME,
            EMAIL,
            PASSWORDHASH,
            ROLE,
            JOINDATE,
            LEAVES_BALANCE
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        return execute_query(
            query,
            [
                name,
                email,
                password_hash,
                role,
                date.today(),
                leave_balance
            ]
        )


class AdminService:

    @staticmethod
    def get_dashboard_stats():

        total_employees = AdminRepository.count_employees()
        pending_leaves = AdminRepository.count_pending_leaves()
        approved_leaves = AdminRepository.count_approved_leaves()

        return {
            "total_employees": total_employees,
            "pending_leaves": pending_leaves,
            "approved_leaves": approved_leaves
        }

    @staticmethod
    def get_all_employees():
        return AdminRepository.get_all_employees()

    @staticmethod
    def create_employee(data):

        if AdminRepository.email_exists(data["email"]):
            return {
                "success": False,
                "message": "Email already exists"
            }

        password_hash = generate_password_hash(data["password"])

        rows = AdminRepository.insert_employee(
            name=data["name"],
            email=data["email"],
            password_hash=password_hash,
            role=data.get("role", "Employee"),
            leave_balance=data.get("leave_balance", 20)
        )

        return {
            "success": rows > 0
        }