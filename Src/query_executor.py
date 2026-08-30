def execute_query(connection, query):

    cursor = connection.cursor()

    try:
        cursor.execute(query)

        result = cursor.fetchall()

        return result

    finally:
        cursor.close()