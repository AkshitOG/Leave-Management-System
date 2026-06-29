from database.connection import get_connection

def execute_query(query:str, params:list|None = None):
    conn = get_connection()
    cursor = conn.cursor()

    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    rows_affected = cursor.rowcount
    conn.commit()

    cursor.close()
    conn.close()
    return rows_affected

def fetchone(query, params:list|None = None):
    conn = get_connection()
    cursor = conn.cursor()

    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def fetchall(query, params:list|None=None):
    conn = get_connection()
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

