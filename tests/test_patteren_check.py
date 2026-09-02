import pytest

from Src.validator import check_pattern
from Src.result_manager import add_result


PATTERNS = {

    "EMAIL":
        r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',

    "PHONE":
        r'^[0-9]{10}$',

    "PINCODE":
        r'^[0-9]{6}$',

    "PAN":
        r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

}


def test_pattern_check(
    snowflake_connection,
    dq_rules
):

    failures = []

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        pattern_name = rule["PATTERN_CHECK"]

        if not pattern_name:
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        try:

            pattern = PATTERNS.get(pattern_name)

            if not pattern:

                raise ValueError(
                    f"Pattern '{pattern_name}' "
                    f"is not configured"
                )

            passed, invalid_count = check_pattern(
                snowflake_connection,
                table_name,
                field_name,
                pattern
            )

            status = "PASS" if passed else "FAIL"

            add_result(
                table_name,
                field_name,
                "PATTERN CHECK",
                pattern_name,
                f"{invalid_count} INVALID",
                status,
                (
                    "Pattern validation passed"
                    if passed
                    else f"{invalid_count} invalid records"
                )
            )

            if not passed:

                failures.append(
                    f"{table_name}.{field_name} "
                    f"has {invalid_count} invalid records"
                )

        except Exception as e:

            add_result(
                table_name,
                field_name,
                "PATTERN CHECK",
                pattern_name,
                "ERROR",
                "FAIL",
                str(e)
            )

            failures.append(
                f"{table_name}.{field_name}: {str(e)}"
            )

    if failures:

        pytest.fail(
            "PATTERN CHECK FAILED:\n"
            + "\n".join(failures)
        )