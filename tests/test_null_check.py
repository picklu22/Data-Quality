import pytest
from Src.validator import check_null
from Src.result_manager import add_result


def test_null_check(
    snowflake_connection,
    dq_rules
):

    failures = []

    for rule in dq_rules:

        # Skip inactive rules
        if rule["IS_ACTIVE"] != "Y":
            continue

        # Skip rows where NULL_CHECK is not enabled
        if rule["NULL_CHECK"] != "Y":
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        try:

            passed, null_count = check_null(
                snowflake_connection,
                table_name,
                field_name
            )

            status = "PASS" if passed else "FAIL"

            add_result(
                table_name,
                field_name,
                "NULL CHECK",
                "0 NULL",
                f"{null_count} NULL",
                status,
                (
                    "No NULL values found"
                    if passed
                    else f"{null_count} NULL values found"
                )
            )

            if not passed:

                failures.append(
                    f"{table_name}.{field_name} "
                    f"has {null_count} NULL values"
                )

        except Exception as e:

            add_result(
                table_name,
                field_name,
                "NULL CHECK",
                "0 NULL",
                "ERROR",
                "FAIL",
                str(e)
            )

            failures.append(
                f"{table_name}.{field_name}: {str(e)}"
            )

    # Assert only after ALL Excel rows are processed
    if failures:

        pytest.fail(
            "NULL CHECK FAILED:\n"
            + "\n".join(failures)
        )