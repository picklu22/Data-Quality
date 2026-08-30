from Src.validator import check_null


def test_null_check(snowflake_connection, dq_rules):

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        if rule["NULL_CHECK"] != "Y":
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        passed, null_count = check_null(
            snowflake_connection,
            table_name,
            field_name
        )

        assert passed, (
            f"{table_name}.{field_name} "
            f"contains {null_count} NULL values"
        )
