# ===========================================================
#  Project   : TestPilot - AI-Powered UI Test Framework
#  File      : test_generator.py
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

import json
import subprocess

PROMPT_TEMPLATE = """
You are a JSON-only generator. 
If you output anything other than a valid JSON array, the response will be rejected. 
Output must start with [ and end with ]. 
Each object must be wrapped in {{}}.
No explanations, no comments, no markdown, no extra text.

You are an AI test generator. Based on the following web page analysis:

Title: {title}
URL: {url}
Possible Actions:
{actions}

Generate a list of UI test cases in pure JSON format.

Each test must have:
- id (string, e.g., T1, T2, …)
- description (string, short and clear)
- action (string: click, fill, goto, check, etc.)
- selector (CSS selector string)
- value (string, leave "" if not needed)
- expected (string, expected outcome)

Output JSON ONLY, like this:

[
  {{
    "id": "T1",
    "description": "Click login button → Login modal opens",
    "action": "click",
    "selector": "button#login",
    "value": "",
    "expected": "Login modal opens"
  }},
  {{
    "id": "T2",
    "description": "Fill username field → Value entered",
    "action": "fill",
    "selector": "input#username",
    "value": "testuser",
    "expected": "Field filled"
  }}
]
"""

def call_ollama(model, prompt):
    """Call Ollama with subprocess and return output"""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        stdout = result.stdout.decode("utf-8").strip()
        stderr = result.stderr.decode("utf-8").strip()

        print("\n--- Ollama Raw Response ---")
        print(stdout)
        print("---------------------------\n")

        if stderr:
            print("\n--- Ollama STDERR ---")
            print(stderr)
            print("---------------------------\n")

        return stdout
    except subprocess.CalledProcessError as e:
        print("❌ Ollama error:", e.stderr.decode())
        return "[]"

def humanize_description(action, selector, value, expected):
    """Make test descriptions human-readable and meaningful"""
    if action == "fill":
        return f"Fill {selector} with '{value}' → {expected}"
    elif action == "check":
        return f"Check option {selector} → {expected}"
    elif action == "click":
        return f"Click {selector} → {expected}"
    elif action == "goto":
        return f"Navigate to {value} → {expected}"
    else:
        return f"{action} on {selector} → {expected}"

def generate_tests(model, analysis):
    actions = analysis.get("actions", [])

    actions_str = "\n".join(
        f"- Action: {a.get('action','')}, Selector: {a.get('selector','')}, Value: {a.get('value','')}"
        for a in actions
    ) or "No actions detected."

    prompt = PROMPT_TEMPLATE.format(
        title=analysis.get("title", "Unknown"),
        url=analysis.get("url", "Unknown"),
        actions=actions_str
    )

    response = call_ollama(model, prompt)

    try:
        tests = json.loads(response)
        if not isinstance(tests, list):
            raise ValueError("Response is not a list")
    except Exception as e:
        print("⚠️ Failed to parse Ollama response, generating tests from analyzer instead. Error:", e)
        tests = []
        for i, a in enumerate(actions, 1):
            tests.append({
                "id": f"T{i}",
                "description": humanize_description(
                    a.get("action", "click"),
                    a.get("selector", "body"),
                    a.get("value", ""),
                    "Expected behavior"
                ),
                "action": a.get("action", "click"),
                "selector": a.get("selector", "body"),
                "value": a.get("value", ""),
                "expected": "Expected behavior"
            })
        return tests

    # Cleanup & humanize descriptions
    for i, t in enumerate(tests, 1):
        t["id"] = t.get("id") or f"T{i}"
        t["action"] = t.get("action") or "click"
        t["selector"] = t.get("selector") or "body"
        t["value"] = t.get("value") or ""
        t["expected"] = t.get("expected") or "Expected behavior"

        desc = t.get("description", "").strip()
        if not desc or desc.lower() in ["test 1", "test 2", ""]:
            t["description"] = humanize_description(
                t["action"], t["selector"], t["value"], t["expected"]
            )

    return tests



# import json
# import subprocess
# import re

# PROMPT_TEMPLATE = """
# You are a JSON-only generator. 
# If you output anything other than a valid JSON array, the response will be rejected. 
# Output must start with [ and end with ]. 
# Each object must be wrapped in {{}}.
# No explanations, no comments, no markdown, no extra text.
# You are an AI test generator. Based on the following web page analysis:

# Title: {title}
# URL: {url}
# Possible Actions:
# {actions}

# Generate one test case PER ACTION above in **pure JSON array format**.
# - Do NOT skip actions.
# - Do NOT return a single object. Must always return a JSON array [].
# - Do NOT prefix with words like "JSON array:" or "JSON object:".
# - Output must start with `[` and end with `]`.

# Each test object MUST have:
# - id (string, e.g., T1, T2, …)
# - description (string, short and clear)
# - action (string: click, fill, goto, check, etc.)
# - selector (CSS selector string)
# - value (string, leave "" if not needed)
# - expected (string, expected outcome)

# Return ONLY a JSON array.
# """

# def call_ollama(model, prompt):
#     try:
#         result = subprocess.run(
#             ["ollama", "run", model],
#             input=prompt.encode("utf-8"),
#             capture_output=True,
#             check=True
#         )
#         stdout = result.stdout.decode("utf-8").strip()
#         stderr = result.stderr.decode("utf-8").strip()

#         print("\n--- Ollama Raw Response ---\n", stdout, "\n---------------------------")
#         if stderr:
#             print("\n--- Ollama STDERR ---\n", stderr, "\n---------------------------")

#         return stdout
#     except subprocess.CalledProcessError as e:
#         print("❌ Ollama error:", e.stderr.decode())
#         return "[]"

# def clean_ollama_json(resp: str) -> str:
#     """Strip junk like 'JSON object:' or 'JSON array:' and extract JSON"""
#     # Grab first valid JSON array
#     match = re.search(r"\[.*\]", resp, re.DOTALL)
#     if match:
#         return match.group(0)
#     # Grab single JSON object and wrap into array
#     match = re.search(r"\{.*\}", resp, re.DOTALL)
#     if match:
#         return "[" + match.group(0) + "]"
#     return "[]"

# def generate_tests(model, analysis):
#     actions = analysis.get("actions", [])

#     actions_str = "\n".join(
#         f"- Action: {a.get('action','')}, Selector: {a.get('selector','')}, Value: {a.get('value','')}"
#         for a in actions
#     ) or "No actions detected."

#     prompt = PROMPT_TEMPLATE.format(
#         title=analysis.get("title", "Unknown"),
#         url=analysis.get("url", "Unknown"),
#         actions=actions_str
#     )

#     response = call_ollama(model, prompt)
#     response = clean_ollama_json(response)

#     try:
#         tests = json.loads(response)

#         if not isinstance(tests, list):
#             raise ValueError("Response is not a JSON array")

#         # Fill in missing keys
#         for i, t in enumerate(tests, 1):
#             t["id"] = str(t.get("id") or f"T{i}")
#             t["action"] = t.get("action") or "click"
#             t["selector"] = t.get("selector") or "body"
#             t["value"] = t.get("value") or ""
#             t["expected"] = t.get("expected") or "Page should respond correctly"

#             if not t.get("description"):
#                 t["description"] = f"{t['action']} on {t['selector']} → {t['expected']}"

#         # ⚠️ If Ollama gave fewer tests than analyzer actions → generate fallbacks
#         if len(tests) < len(actions):
#             print("⚠️ Ollama returned fewer tests than actions, filling in missing ones…")
#             for i, a in enumerate(actions, 1):
#                 if i > len(tests):
#                     tests.append({
#                         "id": f"T{i}",
#                         "description": f"{a.get('action','')} on {a.get('selector','')} → Expected behavior",
#                         "action": a.get("action", "click"),
#                         "selector": a.get("selector", "body"),
#                         "value": a.get("value", ""),
#                         "expected": "Page responds correctly"
#                     })

#         return tests

#     except Exception as e:
#         print("⚠️ Failed to parse Ollama response, generating tests from analyzer instead. Error:", e)
#         # ✅ Direct fallback: generate tests from analyzer actions
#         tests = []
#         for i, a in enumerate(actions, 1):
#             tests.append({
#                 "id": f"T{i}",
#                 "description": f"{a.get('action','')} on {a.get('selector','')} → Expected behavior",
#                 "action": a.get("action", "click"),
#                 "selector": a.get("selector", "body"),
#                 "value": a.get("value", ""),
#                 "expected": "Page responds correctly"
#             })
#         return tests