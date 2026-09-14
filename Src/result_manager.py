import os
from datetime import datetime


RESULTS = []


def add_result(
    table_name,
    field_name,
    check_type,
    expected,
    actual,
    status,
    message=""
):

    RESULTS.append({
        "table_name": table_name,
        "field_name": field_name,
        "check_type": check_type,
        "expected": expected,
        "actual": actual,
        "status": status,
        "message": message
    })


def get_results():

    return RESULTS


def generate_html_report():

    total = len(RESULTS)

    passed = sum(
        1 for result in RESULTS
        if str(result.get("status", "")).upper() == "PASS"
    )

    failed = sum(
        1 for result in RESULTS
        if str(result.get("status", "")).upper() == "FAIL"
    )

    if total > 0:
        pass_percentage = round(
            (passed / total) * 100,
            2
        )
    else:
        pass_percentage = 0

    max_bar_value = max(1, total)
    pass_height = (passed / max_bar_value) * 100
    fail_height = (failed / max_bar_value) * 100

    execution_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    type_summary = {}

    for result in RESULTS:

        check_type = result["check_type"].upper()
        status_key = str(result.get("status", "")).upper()

        if check_type not in type_summary:
            type_summary[check_type] = {
                "PASS": 0,
                "FAIL": 0
            }

        if status_key in {"PASS", "FAIL"}:
            type_summary[check_type][status_key] = (
                type_summary[check_type].get(status_key, 0) + 1
            )

    rows = ""

    for result in RESULTS:

        status_class = (
            "pass"
            if str(result.get("status", "")).upper() == "PASS"
            else "fail"
        )

        rows += f"""
        <tr>

            <td>{result["table_name"]}</td>

            <td>{result["field_name"]}</td>

            <td>{result["check_type"]}</td>

            <td>{result["expected"]}</td>

            <td>{result["actual"]}</td>

            <td>
                <span class="status {status_class}">
                    {result["status"]}
                </span>
            </td>

            <td>{result["message"]}</td>

        </tr>
        """

    type_chart_rows = ""

    if type_summary:
        for check_name in sorted(type_summary):
            stats = type_summary[check_name]
            total_for_type = sum(stats.values())
            pass_count = stats.get("PASS", 0)
            fail_count = stats.get("FAIL", 0)
            type_pass_percentage = (
                round((pass_count / total_for_type) * 100, 2)
                if total_for_type else 0
            )
            type_fail_percentage = (
                round((fail_count / total_for_type) * 100, 2)
                if total_for_type else 0
            )

            type_chart_rows += f"""
            <div class="type-row">
                <div class="type-label">{check_name}</div>
                <div class="type-bar">
                    <span class="type-pass" style="width: {type_pass_percentage}%">{pass_count}</span>
                    <span class="type-fail" style="width: {type_fail_percentage}%">{fail_count}</span>
                </div>
            </div>
            """

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>Data Quality Report</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f4f6f9;

    color: #333;

}}

.header {{

    background: #1f2937;

    color: white;

    padding: 25px 40px;

}}

.header h1 {{

    margin: 0;

    font-size: 28px;

}}

.header p {{

    margin-top: 8px;

    color: #d1d5db;

}}

.container {{

    padding: 30px 40px;

}}

.cards {{

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 20px;

    margin-bottom: 30px;

}}

.card {{

    background: white;

    padding: 22px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0,0,0,0.08);

}}

.card-title {{

    color: #6b7280;

    font-size: 14px;

}}

.card-value {{

    font-size: 30px;

    font-weight: bold;

    margin-top: 8px;

}}

.total {{
    color: #2563eb;
}}

.pass-value {{
    color: #16a34a;
}}

.fail-value {{
    color: #dc2626;
}}

.percentage {{
    color: #7c3aed;
}}

.report-box {{

    background: white;

    padding: 25px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0,0,0,0.08);

}}

.chart-panel {{

    margin-bottom: 25px;

}}

.chart-wrap {{

    display: flex;
    align-items: end;
    gap: 18px;
    height: 180px;
    padding: 20px 10px 10px;
    border-radius: 12px;
    background: linear-gradient(180deg, #f8fafc, #eef2ff);
    border: 1px solid #e5e7eb;

}}

.bar-group {{

    display: flex;
    align-items: end;
    gap: 20px;
    width: 100%;
    height: 100%;

}}

.bar {{

    flex: 1;
    min-height: 8px;
    border-radius: 10px 10px 0 0;
    position: relative;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    color: #111827;
    font-size: 12px;
    font-weight: bold;
    padding-top: 8px;
    box-shadow: inset 0 -2px 0 rgba(0,0,0,0.06);

}}

.pass-bar {{

    background: linear-gradient(180deg, #4ade80, #16a34a);

}}

.fail-bar {{

    background: linear-gradient(180deg, #fca5a5, #ef4444);

}}

.legend {{

    display: flex;
    gap: 20px;
    margin-top: 12px;
    color: #374151;
    font-size: 13px;
    flex-wrap: wrap;

}}

.legend-item {{

    display: flex;
    align-items: center;
    gap: 8px;

}}

.legend-dot {{

    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;

}}

.type-chart {{

    margin-top: 15px;

}}

.type-row {{

    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;

}}

.type-label {{

    min-width: 150px;
    font-size: 12px;
    font-weight: bold;
    color: #374151;
    text-transform: uppercase;

}}

.type-bar {{

    flex: 1;
    display: flex;
    height: 18px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #d1d5db;
    background: #e5e7eb;
    min-width: 120px;

}}

.type-pass {{

    background: linear-gradient(90deg, #4ade80, #16a34a);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    font-weight: bold;
    min-width: 0;

}}

.type-fail {{

    background: linear-gradient(90deg, #fca5a5, #ef4444);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    font-weight: bold;
    min-width: 0;

}}

.report-box h2 {{

    margin-top: 0;

}}

table {{

    width: 100%;

    border-collapse: collapse;

    margin-top: 20px;

}}

th {{

    background: #374151;

    color: white;

    padding: 13px;

    text-align: left;

    font-size: 13px;

}}

td {{

    padding: 12px;

    border-bottom:
        1px solid #e5e7eb;

    font-size: 13px;

}}

tr:hover {{

    background: #f9fafb;

}}

.status {{

    padding: 5px 12px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: bold;

}}

.status.pass {{

    background: #dcfce7;

    color: #166534;

}}

.status.fail {{

    background: #fee2e2;

    color: #991b1b;

}}

.footer {{

    margin-top: 25px;

    color: #6b7280;

    font-size: 12px;

}}

@media(max-width: 900px) {{

    .cards {{

        grid-template-columns:
            repeat(2, 1fr);

    }}

}}

</style>

</head>


<body>


<div class="header">

    <h1>
        Data Quality Validation Report
    </h1>

    <p>
        ETL Data Quality Analyzer
        | Executed: {execution_time}
    </p>

</div>


<div class="container">


<div class="cards">


<div class="card">

    <div class="card-title">
        TOTAL CHECKS
    </div>

    <div class="card-value total">
        {total}
    </div>

</div>


<div class="card">

    <div class="card-title">
        PASSED
    </div>

    <div class="card-value pass-value">
        {passed}
    </div>

</div>


<div class="card">

    <div class="card-title">
        FAILED
    </div>

    <div class="card-value fail-value">
        {failed}
    </div>

</div>


<div class="card">

    <div class="card-title">
        PASS RATE
    </div>

    <div class="card-value percentage">
        {pass_percentage}%
    </div>

</div>


</div>


<div class="report-box chart-panel">

<h2>
    Quality Summary
</h2>

<div class="chart-wrap">

    <div class="bar-group">

        <div class="bar pass-bar" style="height: {pass_height}%">
            {passed}
        </div>

        <div class="bar fail-bar" style="height: {fail_height}%">
            {failed}
        </div>

    </div>

</div>

<div class="legend">

    <div class="legend-item">
        <span class="legend-dot" style="background: #16a34a;"></span>
        Passed ({passed})
    </div>

    <div class="legend-item">
        <span class="legend-dot" style="background: #ef4444;"></span>
        Failed ({failed})
    </div>

</div>

</div>


<div class="report-box">

<h2>
    Test Wise Summary
</h2>

<div class="type-chart">

{type_chart_rows}

</div>

</div>


<div class="report-box">

<h2>
    Validation Details
</h2>


<table>

<thead>

<tr>

<th>Table</th>

<th>Field</th>

<th>Check</th>

<th>Expected</th>

<th>Actual</th>

<th>Status</th>

<th>Message</th>

</tr>

</thead>


<tbody>

{rows}

</tbody>

</table>


<div class="footer">

Generated by ETL Data Quality Analyzer

</div>


</div>


</div>


</body>

</html>
"""

    os.makedirs(
        "Report",
        exist_ok=True
    )

    report_path = (
        "Report/data_quality_report.html"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    return report_path
