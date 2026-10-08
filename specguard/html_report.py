from pathlib import Path
from html import escape


def generate_html_report(
    requirements,
    requirement_map,
    changes,
    reviewed_requirements,
    output_file
):
    """
    Generate an HTML dashboard containing requirement coverage,
    traceability, change-impact information, and review status.
    """

    total = len(requirements)

    covered = sum(
        1
        for requirement in requirements
        if requirement_map.get(requirement["id"], [])
    )

    missing = total - covered
    coverage = (covered / total * 100) if total else 0

    # ---------------------------------------------------------
    # Build requirement traceability table
    # ---------------------------------------------------------

    requirement_rows = ""

    for requirement in requirements:
        requirement_id = requirement["id"]
        title = requirement["title"]
        priority = requirement.get("priority", "unknown")

        tests = requirement_map.get(requirement_id, [])

        if tests:
            status = "COVERED"
            status_class = "covered"
        else:
            status = "MISSING"
            status_class = "missing"

        test_names = "<br>".join(
            escape(test)
            for test in tests
        )

        if not test_names:
            test_names = "No tests found"

        requirement_rows += f"""
        <tr>
            <td>{escape(requirement_id)}</td>
            <td>{escape(title)}</td>
            <td>{escape(priority.upper())}</td>
            <td class="{status_class}">
                {status}
            </td>
            <td>{len(tests)}</td>
            <td>{test_names}</td>
        </tr>
        """

    # ---------------------------------------------------------
    # Build change-impact section
    # ---------------------------------------------------------

    change_cards = ""

    for change in changes["modified"]:
        requirement_id = change["id"]

        old_description = change["old"]["description"].strip()
        new_description = change["new"]["description"].strip()

        associated_tests = requirement_map.get(
            requirement_id,
            []
        )

        if requirement_id in reviewed_requirements:
            review_status = "REVIEWED"
            review_class = "reviewed"
        else:
            review_status = "REVIEW REQUIRED"
            review_class = "review-required"

        test_list = "".join(
            f"<li>{escape(test)}</li>"
            for test in associated_tests
        )

        if not test_list:
            test_list = "<li>No associated tests found</li>"

        change_cards += f"""
        <div class="change-card">
            <div class="change-header">
                <h3>{escape(requirement_id)}</h3>
                <span class="badge {review_class}">
                    {review_status}
                </span>
            </div>

            <div class="comparison">
                <div>
                    <h4>Old Requirement</h4>
                    <p>{escape(old_description)}</p>
                </div>

                <div>
                    <h4>New Requirement</h4>
                    <p>{escape(new_description)}</p>
                </div>
            </div>

            <h4>Impacted Tests ({len(associated_tests)})</h4>

            <ul>
                {test_list}
            </ul>
        </div>
        """

    if not change_cards:
        change_cards = """
        <div class="no-changes">
            No modified requirements detected.
        </div>
        """

    # ---------------------------------------------------------
    # Complete HTML document
    # ---------------------------------------------------------

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>SpecGuard QA Report</title>

<style>

    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: #f4f6f8;
        color: #1f2937;
    }}

    .container {{
        width: 92%;
        max-width: 1200px;
        margin: 40px auto;
    }}

    .header {{
        margin-bottom: 30px;
    }}

    .header h1 {{
        margin-bottom: 8px;
    }}

    .header p {{
        color: #6b7280;
        margin-top: 0;
    }}

    .cards {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 35px;
    }}

    .card {{
        background: white;
        padding: 22px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }}

    .card .label {{
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 10px;
    }}

    .card .value {{
        font-size: 30px;
        font-weight: bold;
    }}

    .section {{
        background: white;
        padding: 24px;
        margin-bottom: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        overflow-x: auto;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }}

    th {{
        text-align: left;
        background: #f9fafb;
        padding: 12px;
        border-bottom: 2px solid #e5e7eb;
    }}

    td {{
        padding: 12px;
        border-bottom: 1px solid #e5e7eb;
        vertical-align: top;
    }}

    .covered {{
        font-weight: bold;
        color: #15803d;
    }}

    .missing {{
        font-weight: bold;
        color: #b91c1c;
    }}

    .change-card {{
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }}

    .change-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .badge {{
        padding: 7px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }}

    .reviewed {{
        background: #dcfce7;
        color: #166534;
    }}

    .review-required {{
        background: #fef3c7;
        color: #92400e;
    }}

    .comparison {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 15px;
    }}

    .comparison div {{
        background: #f9fafb;
        padding: 16px;
        border-radius: 7px;
    }}

    .no-changes {{
        padding: 18px;
        background: #f9fafb;
        border-radius: 7px;
    }}

    @media (max-width: 800px) {{

        .cards {{
            grid-template-columns: 1fr 1fr;
        }}

        .comparison {{
            grid-template-columns: 1fr;
        }}
    }}

</style>

</head>

<body>

<div class="container">

    <div class="header">
        <h1>SpecGuard</h1>
        <p>Automated Requirement Coverage & Change Impact Analysis</p>
    </div>

    <div class="cards">

        <div class="card">
            <div class="label">Total Requirements</div>
            <div class="value">{total}</div>
        </div>

        <div class="card">
            <div class="label">Coverage</div>
            <div class="value">{coverage:.1f}%</div>
        </div>

        <div class="card">
            <div class="label">Missing Requirements</div>
            <div class="value">{missing}</div>
        </div>

        <div class="card">
            <div class="label">Modified Requirements</div>
            <div class="value">{len(changes["modified"])}</div>
        </div>

    </div>

    <div class="section">

        <h2>Requirement Traceability</h2>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Requirement</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Tests</th>
                    <th>Mapped Test Cases</th>
                </tr>
            </thead>

            <tbody>
                {requirement_rows}
            </tbody>

        </table>

    </div>

    <div class="section">

        <h2>Change Impact Analysis</h2>

        <p>
            Added: {len(changes["added"])}
            &nbsp; | &nbsp;
            Removed: {len(changes["removed"])}
            &nbsp; | &nbsp;
            Modified: {len(changes["modified"])}
        </p>

        {change_cards}

    </div>

</div>

</body>

</html>
"""

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        html,
        encoding="utf-8"
    )