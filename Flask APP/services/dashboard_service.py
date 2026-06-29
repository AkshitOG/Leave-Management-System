from database.db_helper import *

class DashboardService:

    @staticmethod
    def get_leave_stats(employee_id:int):
        query = """SELECT STATUS,COUNT(*)
        FROM LeaveRequests
        WHERE EMPLOYEEID = ?
        GROUP BY STATUS"""

        rows = fetchall(query, employee_id)

        stats = {
            "Pending": 0,
            "Approved": 0,
            "Rejected": 0,
            "Cancelled": 0
        }

        for row in rows:
            stats[row.STATUS.capitalize()] = row[1]

        stats["Total"] = (
            stats["Pending"]
            + stats["Approved"]
            + stats["Rejected"]
            + stats["Cancelled"]
        )

        return stats