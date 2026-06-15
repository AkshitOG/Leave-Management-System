import pyodbc
import os
from dotenv import load_dotenv
from connection import get_connection

load_dotenv()

def create_db_if_not():
    conn, cursor = None, None
    try:
        connection_string = (
            f"Driver={{{os.getenv('Database_drivers')}}};"
            f"Server={os.getenv('Server')};"
            f"Database=master;"
            f"UID={os.getenv('Database_uid')};"
            f"PWD={os.getenv('Database_password')};"
            "TrustServerCertificate=yes;"
        )

        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            IF DB_ID('{os.getenv('Database')}') IS NULL
            BEGIN
                CREATE DATABASE [{os.getenv('Database')}]
            END
        """)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def create_tables():
    queries = [
        f"""IF OBJECT_ID('Employees', 'U') IS NULL
            BEGIN
                CREATE TABLE Employees (
                    EMPLOYEEID INT IDENTITY(1,1) PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    EMAIL VARCHAR(200) NOT NULL UNIQUE,
                    PASSWORDHASH VARCHAR(255) NOT NULL,
                    ROLE VARCHAR(20) NOT NULL CHECK (ROLE IN ('Employee','HR','Admin')),
                    JOINDATE DATE NOT NULL
            )
        END""",
        f"""IF OBJECT_ID('LeaveRequests', 'U') IS NULL
        BEGIN
            CREATE TABLE LeaveRequests (
                REQUESTID INT IDENTITY(1,1) PRIMARY KEY,
                EMPLOYEEID INT NOT NULL,
                LEAVETYPE VARCHAR(50),
                STARTDATE DATE NOT NULL,
                ENDDATE DATE NOT NULL,
                REASON VARCHAR(500),
                STATUS VARCHAR(50) DEFAULT 'Pending' CHECK (STATUS IN ('Pending','Approved','Rejected','Cancelled')),
                CREATEDATE DATETIME DEFAULT GETDATE(),

                FOREIGN KEY (EMPLOYEEID)
                    REFERENCES Employees(EMPLOYEEID)
            )
        END""",
        f"""IF OBJECT_ID('Approvals','U') IS NULL
        BEGIN
            CREATE TABLE Approvals (
                APPROVALID INT IDENTITY(1,1) PRIMARY KEY,
                REQUESTID INT NOT NULL,
                APPROVEDBY INT NOT NULL,
                DECISION VARCHAR(20),
                COMMENTS VARCHAR(500),
                APPROVALDATE DATETIME DEFAULT GETDATE(),

                FOREIGN KEY (REQUESTID)
                    REFERENCES LeaveRequests(REQUESTID),
                
                FOREIGN KEY (APPROVEDBY)
                    REFERENCES Employees(EMPLOYEEID)
            )
        END"""
    ]

    conn = get_connection()
    cursor = conn.cursor()
    for query in queries:
        cursor.execute(query)

    conn.commit()

    cursor.close()
    conn.close()

