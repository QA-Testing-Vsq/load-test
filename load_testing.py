import threading
import urllib.request
import time
import html
from datetime import datetime
 
 
# ============================================================
# CONFIGURATION
# ============================================================
 
URL = "https://publicsafety-ssledev-dyhneabchcgcg5e0.westus-01.azurewebsites.net/incident-response-time"
 
CONCURRENT_USERS = 10000
TIMEOUT_SECONDS = 10
 
REPORT_FILE = "load_test_report.html"
 
 
# ============================================================
# SHARED DATA
# ============================================================
 
results = []
results_lock = threading.Lock()
 
 
# ============================================================
# SEND REQUEST
# ============================================================
 
def hit_url(user_id):
    start = time.perf_counter()
 
    try:
        req = urllib.request.Request(
            URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
 
        with urllib.request.urlopen(
            req,
            timeout=TIMEOUT_SECONDS
        ) as response:
 
            status_code = response.status
 
            # Read response so the request is fully completed
            response.read()
 
        elapsed = round(
            (time.perf_counter() - start) * 1000,
            2
        )
 
        result = {
            "status": "PASS",
            "user_id": user_id,
            "response_time": elapsed,
            "status_code": status_code,
            "error": ""
        }
 
        with results_lock:
            results.append(result)
 
        print(
            f"User {user_id:>3} → PASS → "
            f"{elapsed:>8} ms → HTTP {status_code}"
        )
 
    except Exception as e:
 
        elapsed = round(
            (time.perf_counter() - start) * 1000,
            2
        )
 
        result = {
            "status": "FAIL",
            "user_id": user_id,
            "response_time": elapsed,
            "status_code": "-",
            "error": str(e)
        }
 
        with results_lock:
            results.append(result)
 
        print(
            f"User {user_id:>3} → FAIL → "
            f"{elapsed:>8} ms → {e}"
        )
 
 
# ============================================================
# GENERATE HTML REPORT
# ============================================================
 
def generate_html_report(
    results,
    total_duration,
    concurrent_users
):
 
    passed = [
        r for r in results
        if r["status"] == "PASS"
    ]
 
    failed = [
        r for r in results
        if r["status"] == "FAIL"
    ]
 
    response_times = [
        r["response_time"]
        for r in passed
    ]
 
    total_users = concurrent_users
    passed_count = len(passed)
    failed_count = len(failed)
 
    error_rate = (
        (failed_count / total_users) * 100
        if total_users > 0
        else 0
    )
 
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        min_response = min(response_times)
        max_response = max(response_times)
    else:
        avg_response = 0
        min_response = 0
        max_response = 0
 
    generated_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
 
    # Sort results by user ID
    sorted_results = sorted(
        results,
        key=lambda x: x["user_id"]
    )
 
    rows = ""
 
    for result in sorted_results:
 
        status = result["status"]
 
        status_class = (
            "pass"
            if status == "PASS"
            else "fail"
        )
 
        error_text = html.escape(
            result["error"]
        )
 
        rows += f"""
<tr>
<td>{result["user_id"]}</td>
 
            <td>
<span class="status {status_class}">
                    {status}
</span>
</td>
 
            <td>{result["response_time"]} ms</td>
 
            <td>{result["status_code"]}</td>
 
            <td>{error_text}</td>
</tr>
        """
 
    html_report = f"""
<!DOCTYPE html>
 
<html lang="en">
 
<head>
 
<meta charset="UTF-8">
 
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">
 
<title>Load Test Report</title>
 
<style>
 
* {{
    box-sizing: border-box;
}}
 
body {{
    margin: 0;
    padding: 30px;
 
    font-family:
        Arial,
        Helvetica,
        sans-serif;
 
    background: #f4f6f8;
    color: #222;
}}
 
.container {{
    max-width: 1200px;
    margin: auto;
}}
 
.header {{
    background: #1f2937;
    color: white;
 
    padding: 30px;
 
    border-radius: 12px;
 
    margin-bottom: 25px;
}}
 
.header h1 {{
    margin: 0 0 10px 0;
}}
 
.header p {{
    margin: 5px 0;
    color: #d1d5db;
}}
 
.summary {{
    display: grid;
 
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
 
    gap: 15px;
 
    margin-bottom: 25px;
}}
 
.card {{
    background: white;
 
    padding: 22px;
 
    border-radius: 10px;
 
    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);
}}
 
.card-title {{
    font-size: 14px;
    color: #6b7280;
 
    margin-bottom: 8px;
}}
 
.card-value {{
    font-size: 28px;
    font-weight: bold;
}}
 
.pass-number {{
    color: #15803d;
}}
 
.fail-number {{
    color: #dc2626;
}}
 
.warning-number {{
    color: #d97706;
}}
 
.section {{
    background: white;
 
    padding: 25px;
 
    border-radius: 10px;
 
    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);
 
    margin-bottom: 25px;
}}
 
.section h2 {{
    margin-top: 0;
}}
 
.info-grid {{
    display: grid;
 
    grid-template-columns:
        repeat(auto-fit, minmax(250px, 1fr));
 
    gap: 15px;
}}
 
.info-item {{
    padding: 15px;
 
    background: #f9fafb;
 
    border-radius: 8px;
}}
 
.info-label {{
    font-size: 13px;
    color: #6b7280;
}}
 
.info-value {{
    margin-top: 5px;
 
    font-weight: bold;
 
    word-break: break-word;
}}
 
table {{
    width: 100%;
 
    border-collapse: collapse;
 
    margin-top: 15px;
}}
 
th {{
    background: #111827;
    color: white;
 
    text-align: left;
 
    padding: 12px;
}}
 
td {{
    padding: 12px;
 
    border-bottom:
        1px solid #e5e7eb;
}}
 
tr:hover {{
    background: #f9fafb;
}}
 
.status {{
    display: inline-block;
 
    padding: 5px 10px;
 
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
    text-align: center;
 
    color: #6b7280;
 
    font-size: 13px;
 
    margin-top: 25px;
}}
 
@media(max-width: 700px) {{
 
    body {{
        padding: 15px;
    }}
 
    table {{
        font-size: 13px;
    }}
 
    th,
    td {{
        padding: 8px;
    }}
 
}}
 
</style>
 
</head>
 
 
<body>
 
<div class="container">
 
 
    <div class="header">
 
        <h1>
            HTTP Concurrent Load Test Report
</h1>
 
        <p>
            Generated: {generated_time}
</p>
 
        <p>
            Target:
            {html.escape(URL)}
</p>
 
    </div>
 
 
    <!-- SUMMARY -->
 
    <div class="summary">
 
 
        <div class="card">
 
            <div class="card-title">
                Total Users
</div>
 
            <div class="card-value">
                {total_users}
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Passed
</div>
 
            <div class="card-value pass-number">
                {passed_count}
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Failed
</div>
 
            <div class="card-value fail-number">
                {failed_count}
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Error Rate
</div>
 
            <div class="card-value warning-number">
                {error_rate:.1f}%
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Average Response
</div>
 
            <div class="card-value">
                {avg_response:.2f} ms
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Maximum Response
</div>
 
            <div class="card-value">
                {max_response:.2f} ms
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Minimum Response
</div>
 
            <div class="card-value">
                {min_response:.2f} ms
</div>
 
        </div>
 
 
        <div class="card">
 
            <div class="card-title">
                Total Duration
</div>
 
            <div class="card-value">
                {total_duration:.2f} sec
</div>
 
        </div>
 
 
    </div>
 
 
    <!-- TEST CONFIGURATION -->
 
    <div class="section">
 
        <h2>
            Test Configuration
</h2>
 
        <div class="info-grid">
 
 
            <div class="info-item">
 
                <div class="info-label">
                    Target URL
</div>
 
                <div class="info-value">
                    {html.escape(URL)}
</div>
 
            </div>
 
 
            <div class="info-item">
 
                <div class="info-label">
                    Concurrent Users
</div>
 
                <div class="info-value">
                    {CONCURRENT_USERS}
</div>
 
            </div>
 
 
            <div class="info-item">
 
                <div class="info-label">
                    Request Timeout
</div>
 
                <div class="info-value">
                    {TIMEOUT_SECONDS} seconds
</div>
 
            </div>
 
 
            <div class="info-item">
 
                <div class="info-label">
                    Test Duration
</div>
 
                <div class="info-value">
                    {total_duration:.2f} seconds
</div>
 
            </div>
 
 
        </div>
 
    </div>
 
 
    <!-- USER RESULTS -->
 
    <div class="section">
 
        <h2>
            Individual User Results
</h2>
 
        <table>
 
            <thead>
 
                <tr>
 
                    <th>
                        User
</th>
 
                    <th>
                        Status
</th>
 
                    <th>
                        Response Time
</th>
 
                    <th>
                        HTTP Status
</th>
 
                    <th>
                        Error
</th>
 
                </tr>
 
            </thead>
 
 
            <tbody>
 
                {rows}
 
            </tbody>
 
        </table>
 
    </div>
 
 
    <div class="footer">
 
        Generated by Python Concurrent HTTP Load Test
 
    </div>
 
 
</div>
 
</body>
 
</html>
"""
 
    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
 
        file.write(html_report)
 
 
# ============================================================
# MAIN TEST
# ============================================================
 
def main():
 
    print()
    print("=" * 60)
    print("CONCURRENT HTTP LOAD TEST")
    print("=" * 60)
 
    print(f"Target URL       : {URL}")
    print(f"Concurrent Users : {CONCURRENT_USERS}")
    print(f"Timeout          : {TIMEOUT_SECONDS} seconds")
    print()
 
    threads = []
 
    start_all = time.perf_counter()
 
    # Create threads
    for i in range(
        1,
        CONCURRENT_USERS + 1
    ):
 
        thread = threading.Thread(
            target=hit_url,
            args=(i,)
        )
 
        threads.append(thread)
 
    # Start all threads
    for thread in threads:
        thread.start()
 
    # Wait for all threads
    for thread in threads:
        thread.join()
 
    total_duration = (
        time.perf_counter() - start_all
    )
 
    # ========================================================
    # CONSOLE SUMMARY
    # ========================================================
 
    passed = [
        r for r in results
        if r["status"] == "PASS"
    ]
 
    failed = [
        r for r in results
        if r["status"] == "FAIL"
    ]
 
    times = [
        r["response_time"]
        for r in passed
    ]
 
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
 
    print(
        f"TOTAL USERS     : {CONCURRENT_USERS}"
    )
 
    print(
        f"PASSED          : {len(passed)}"
    )
 
    print(
        f"FAILED          : {len(failed)}"
    )
 
    print(
        f"ERROR RATE      : "
        f"{len(failed) / CONCURRENT_USERS * 100:.1f}%"
    )
 
    if times:
 
        print(
            f"AVG RESPONSE    : "
            f"{sum(times) / len(times):.2f} ms"
        )
 
        print(
            f"MAX RESPONSE    : "
            f"{max(times):.2f} ms"
        )
 
        print(
            f"MIN RESPONSE    : "
            f"{min(times):.2f} ms"
        )
 
    print(
        f"TOTAL DURATION  : "
        f"{total_duration:.2f} sec"
    )
 
    print("=" * 60)
 
    # ========================================================
    # GENERATE REPORT
    # ========================================================
 
    generate_html_report(
        results,
        total_duration,
        CONCURRENT_USERS
    )
 
    print()
    print(
        f"HTML REPORT CREATED: {REPORT_FILE}"
    )
 
 
# ============================================================
# RUN
# ============================================================
 
if __name__ == "__main__":
    main()