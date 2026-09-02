import pytest

from Src.validator import check_duplicate
from Src.result_manager import add_result


def test_duplicate_check(
    snowflake_connection,
    dq_rules
):

    failures = []

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        if rule["DUPLICATE_CHECK"] != "Y":
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        try:

            passed, duplicate_count = check_duplicate(
                snowflake_connection,
                table_name,
                field_name
            )

            status = "PASS" if passed else "FAIL"

            add_result(
                table_name,
                field_name,
                "DUPLICATE CHECK",
                "0 DUPLICATES",
                f"{duplicate_count} DUPLICATES",
                status,
                (
                    "No duplicates found"
                    if passed
                    else f"{duplicate_count} duplicate values found"
                )
            )

            if not passed:

                failures.append(
                    f"{table_name}.{field_name} "
                    f"has {duplicate_count} duplicates"
                )

        except Exception as e:

            add_result(
                table_name,
                field_name,
                "DUPLICATE CHECK",
                "0 DUPLICATES",
                "ERROR",
                "FAIL",
                str(e)
            )

            failures.append(
                f"{table_name}.{field_name}: {str(e)}"
            )

    if failures:

        pytest.fail(
            "DUPLICATE CHECK FAILED:\n"
            + "\n".join(failures)
        )