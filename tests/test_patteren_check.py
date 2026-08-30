from Src.validator import check_pattern


PATTERNS = {

    "EMAIL":
        r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',

    "PHONE":
        r'^[0-9]{10}$'
}


def test_pattern_check(snowflake_connection, dq_rules):

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        pattern_name = rule["PATTERN_CHECK"]

        if not pattern_name:
            continue

        pattern = PATTERNS.get(pattern_name)

        if not pattern:
            raise ValueError(
                f"Unknown pattern: {pattern_name}"
            )

        passed, invalid_count = check_pattern(
            snowflake_connection,
            rule["TABLE_NAME"],
            rule["FIELD_NAME"],
            pattern
        )

        assert passed, (
            f"{rule['TABLE_NAME']}.{rule['FIELD_NAME']} "
            f"has {invalid_count} invalid records"
        )