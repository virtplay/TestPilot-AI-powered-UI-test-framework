# ===========================================================
#  Project   : TestPilot - AI-Powered UI Test Framework
#  File      : analyser.py
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


import asyncio
from playwright.async_api import async_playwright

async def analyze_page(url, max_elements=200):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="load", timeout=30000)
        title = await page.title()
        url_final = page.url

        elements = await page.query_selector_all(
            "a, button, input, select, textarea, [role='button'], form, [data-testid]"
        )
        actions = []

        for i, el in enumerate(elements[:max_elements]):
            try:
                tag = await el.evaluate("(e) => e.tagName.toLowerCase()")
                attrs = await el.evaluate("""(e) => {
                    const a = {};
                    for (const at of e.attributes) a[at.name] = at.value;
                    return a;
                }""")

                # Build a usable selector
                if "id" in attrs:
                    selector = f"#{attrs['id']}"
                elif "name" in attrs:
                    selector = f"[name='{attrs['name']}']"
                elif "class" in attrs:
                    selector = f".{attrs['class'].split()[0]}"
                else:
                    selector = tag

                # Map elements → actions
                if tag == "input":
                    t = attrs.get("type", "text")
                    if t in ["text", "email", "password", "number"]:
                        actions.append({"action": "fill", "selector": selector, "value": f"sample_{t}_{i}"})
                    elif t in ["checkbox", "radio"]:
                        actions.append({"action": "check", "selector": selector, "value": "true"})
                    elif t in ["submit", "button"]:
                        actions.append({"action": "click", "selector": selector, "value": ""})
                elif tag == "textarea":
                    actions.append({"action": "fill", "selector": selector, "value": f"sample_text_{i}"})
                elif tag == "select":
                    actions.append({"action": "select", "selector": selector, "value": "first_option"})
                elif tag in ["button", "a"] or attrs.get("role") == "button":
                    actions.append({"action": "click", "selector": selector, "value": ""})

            except Exception:
                continue

        screenshot_path = "page_capture.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()

        # 📝 Debug log
        print("\n--- Analyzer Results ---")
        print(f"Page Title: {title}")
        print(f"Final URL: {url_final}")
        print(f"Detected {len(actions)} actions:")
        for a in actions:
            print(" ", a)
        print("------------------------\n")

        return {
            "title": title,
            "url": url_final,
            "actions": actions,
            "screenshot": screenshot_path
        }

def run(url):
    return asyncio.run(analyze_page(url))
