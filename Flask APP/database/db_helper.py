from connection import get_connection

def execute_query(query:str, params:bool = None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params or [])
    cursor.commit()

    cursor.close()
    conn.close()

def fetchone(query, params = None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params or [])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def fetchall(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

