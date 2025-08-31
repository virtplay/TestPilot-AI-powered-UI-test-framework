# ===========================================================
#  Project   : TestPilot - AI-Powered UI Test Framework
#  File      : report.py
#  Author    : Karthik Bs
#  Created   : 31-Aug-2025
#  Version   : 1.0
# ===========================================================
#  Description:
#    This module is part of TestPilot, an AI-driven UI testing
#    framework that analyzes web pages, generates test cases
#    via LLM (Ollama), executes them with Playwright, and
#    produces human-readable reports.

#  License:
#    This project is open-source under the MIT License.
# ===========================================================

import json, os, datetime
def make_report(results, out_dir="results"):
    os.makedirs(out_dir, exist_ok=True)
    now = datetime.datetime.utcnow().isoformat()
    with open(os.path.join(out_dir, "report.json"), "w") as f:
        json.dump({"generated_at": now,"results": results}, f, indent=2)
    rows = ""
    for r in results:
        color = "green" if r["status"]=="passed" else "red"
        err = r.get("error") or ""
        rows += f"<tr><td>{r['id']}</td><td>{r['description']}</td><td style='color:{color}'>{r['status']}</td><td>{err}</td></tr>\n"
    html = f"""
    <html><head><title>AI UI Test Report</title></head><body>
    <h1>AI UI Test Report</h1><p>Generated: {now}</p>
    <table border='1' cellpadding='6'>
    <tr><th>ID</th><th>Description</th><th>Status</th><th>Error</th></tr>
    {rows}
    </table></body></html>
    """
    with open(os.path.join(out_dir, "report.html"), "w") as f:
        f.write(html)
    print("Report created:", os.path.abspath(out_dir))
