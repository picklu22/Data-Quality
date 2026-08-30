from Src.validator import check_outlier


def test_outlier_check(snowflake_connection, dq_rules):

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        if rule["OUTLIER"] != "Y":
            continue

        passed, outlier_count = check_outlier(
            snowflake_connection,
            rule["TABLE_NAME"],
            rule["FIELD_NAME"]
        )

        assert passed, (
            f"{rule['TABLE_NAME']}.{rule['FIELD_NAME']} "
            f"contains {outlier_count} outliers"
        )