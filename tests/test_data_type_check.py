from Src.validator import check_datatype


def test_datatype_check(snowflake_connection, dq_rules):

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        expected_type = rule["DATATYPE"]

        if not expected_type:
            continue

        passed, actual_type = check_datatype(
            snowflake_connection,
            rule["TABLE_NAME"],
            rule["FIELD_NAME"],
            expected_type
        )

        assert passed, (
            f"{rule['TABLE_NAME']}.{rule['FIELD_NAME']} "
            f"expected {expected_type} "
            f"but found {actual_type}"
        )