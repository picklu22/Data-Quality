from Src.validator import check_duplicate


def test_duplicate_check(snowflake_connection, dq_rules):

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        if rule["DUPLICATE_CHECK"] != "Y":
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        passed, duplicate_count = check_duplicate(
            snowflake_connection,
            table_name,
            field_name
        )

        assert passed, (
            f"{table_name}.{field_name} "
            f"contains {duplicate_count} duplicate values"
        )