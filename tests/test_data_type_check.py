import pytest

from Src.validator import check_datatype
from Src.result_manager import add_result


def test_datatype_check(
    snowflake_connection,
    dq_rules
):

    failures = []

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        expected_type = rule["DATATYPE"]

        if not expected_type:
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        try:

            passed, actual_type = check_datatype(
                snowflake_connection,
                table_name,
                field_name,
                expected_type
            )

            status = "PASS" if passed else "FAIL"

            add_result(
                table_name,
                field_name,
                "DATATYPE CHECK",
                expected_type,
                actual_type,
                status,
                (
                    "Datatype matches"
                    if passed
                    else "Datatype mismatch"
                )
            )

            if not passed:

                failures.append(
                    f"{table_name}.{field_name}: "
                    f"Expected {expected_type}, "
                    f"Actual {actual_type}"
                )

        except Exception as e:

            add_result(
                table_name,
                field_name,
                "DATATYPE CHECK",
                expected_type,
                "ERROR",
                "FAIL",
                str(e)
            )

            failures.append(
                f"{table_name}.{field_name}: {str(e)}"
            )

    if failures:

        pytest.fail(
            "DATATYPE CHECK FAILED:\n"
            + "\n".join(failures)
        )