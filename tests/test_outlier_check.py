import pytest

from Src.validator import check_outlier
from Src.result_manager import add_result


def test_outlier_check(
    snowflake_connection,
    dq_rules
):

    failures = []

    for rule in dq_rules:

        if rule["IS_ACTIVE"] != "Y":
            continue

        if rule["OUTLIER"] != "Y":
            continue

        table_name = rule["TABLE_NAME"]
        field_name = rule["FIELD_NAME"]

        try:

            passed, outlier_count = check_outlier(
                snowflake_connection,
                table_name,
                field_name
            )

            status = "PASS" if passed else "FAIL"

            add_result(
                table_name,
                field_name,
                "OUTLIER CHECK",
                "0 OUTLIERS",
                f"{outlier_count} OUTLIERS",
                status,
                (
                    "No outliers found"
                    if passed
                    else f"{outlier_count} outliers found"
                )
            )

            if not passed:

                failures.append(
                    f"{table_name}.{field_name} "
                    f"has {outlier_count} outliers"
                )

        except Exception as e:

            add_result(
                table_name,
                field_name,
                "OUTLIER CHECK",
                "0 OUTLIERS",
                "ERROR",
                "FAIL",
                str(e)
            )

            failures.append(
                f"{table_name}.{field_name}: {str(e)}"
            )

    if failures:

        pytest.fail(
            "OUTLIER CHECK FAILED:\n"
            + "\n".join(failures)
        )