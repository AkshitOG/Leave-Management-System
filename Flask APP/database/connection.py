import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pyodbc.connect(f'Driver={{{os.getenv("Database_drivers")}}};'
                          f'Server={os.getenv("Server")};'
                          f'Database={os.getenv("Database")};'
                          f'UID={os.getenv("Database_uid")};'
                          f'PWD={os.getenv("Database_password")};'
                          'TrustServerCertificate=yes')

