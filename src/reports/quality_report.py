from datetime import datetime
from jinja2 import Template

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Quality Report - {{ suite_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        .pass { color: green; }
        .fail { color: red; }
        .summary { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Data Quality Report</h1>
    <p>Suite: <strong>{{ suite_name }}</strong></p>
    <p>Generated: {{ timestamp }}</p>

    <div class="summary">
        <h2>Summary</h2>
        <p>Total: {{ total }} | Passed: <span class="pass">{{ passed }}</span> | Failed: <span class="fail">{{ failed }}</span></p>
        <p>Success Rate: {{ "%.1f"|format(success_rate) }}%</p>
    </div>

    <h2>Results</h2>
    <table>
        <tr><th>Expectation</th><th>Status</th><th>Details</th></tr>
        {% for r in results %}
        <tr>
            <td>{{ r.expectation }}</td>
            <td class="{{ 'pass' if r.success else 'fail' }}">{{ 'PASS' if r.success else 'FAIL' }}</td>
            <td>{{ r.kwargs }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


def generate_html_report(suite_name: str, results: dict, output_path: str = "quality_report.html"):
    template = Template(REPORT_TEMPLATE)
    html = template.render(
        suite_name=suite_name,
        timestamp=datetime.utcnow().isoformat(),
        total=results["total"],
        passed=results["passed"],
        failed=results["failed"],
        success_rate=results["success_rate"],
        results=results["results"],
    )

    with open(output_path, "w") as f:
        f.write(html)

    return output_path
