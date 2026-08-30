from Src.query_executor import execute_query


def check_null(connection, table_name, field_name):

    query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE {field_name} IS NULL
    """

    result = execute_query(connection, query)

    null_count = result[0][0]

    return null_count == 0, null_count


def check_duplicate(connection, table_name, field_name):

    query = f"""
        SELECT COUNT(*)
        FROM (
            SELECT {field_name}
            FROM {table_name}
            GROUP BY {field_name}
            HAVING COUNT(*) > 1
        )
    """

    result = execute_query(connection, query)

    duplicate_count = result[0][0]

    return duplicate_count == 0, duplicate_count


def check_pattern(connection, table_name, field_name, pattern):

    query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE NOT REGEXP_LIKE(
            {field_name},
            '{pattern}'
        )
    """

    result = execute_query(connection, query)

    invalid_count = result[0][0]

    return invalid_count == 0, invalid_count


def check_datatype(connection, table_name, field_name, expected_type):

    query = f"""
        SELECT DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        AND COLUMN_NAME = '{field_name}'
    """

    result = execute_query(connection, query)

    if not result:
        return False, "COLUMN NOT FOUND"

    actual_type = result[0][0]

    return (
        actual_type.upper() == expected_type.upper(),
        actual_type
    )


def check_outlier(connection, table_name, field_name):

    query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE {field_name} < (
            SELECT AVG({field_name}) -
                   3 * STDDEV({field_name})
            FROM {table_name}
        )
        OR {field_name} > (
            SELECT AVG({field_name}) +
                   3 * STDDEV({field_name})
            FROM {table_name}
        )
    """

    result = execute_query(connection, query)

    outlier_count = result[0][0]

    return outlier_count == 0, outlier_count