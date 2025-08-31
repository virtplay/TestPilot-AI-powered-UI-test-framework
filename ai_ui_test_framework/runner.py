# ===========================================================
#  Project   : TestPilot - AI-Powered UI Test Framework
#  File      : runner.py
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

import asyncio, json, os, time
from playwright.async_api import async_playwright

async def perform_step(page, step):
    action = step.get("action")
    selector = step.get("selector")
    value = step.get("value")
    if action=="click":
        await page.click(selector, timeout=10000)
    elif action=="fill":
        await page.fill(selector, value, timeout=10000)
    elif action=="assert_text":
        el = await page.query_selector(selector)
        text = (await el.inner_text()).strip()
        assert value in text, f"assert_text failed: expected '{value}' in '{text}'"
    elif action=="assert_url":
        assert value in page.url, f"assert_url failed: expected '{value}' in {page.url}"
    elif action=="wait":
        await page.wait_for_selector(selector, timeout=10000)
    else:
        raise RuntimeError("Unknown action " + str(action))

async def run_tests(url, tests, screenshots_dir="results"):
    os.makedirs(screenshots_dir, exist_ok=True)
    results = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, wait_until="load", timeout=30000)
        for t in tests:
            tid = t.get("id")
            desc = t.get("description")
            start = time.time()
            status = "passed"
            error = None
            try:
                for step in t.get("steps", []):
                    await perform_step(page, step)
            except Exception as e:
                status = "failed"
                error = str(e)
                shot = os.path.join(screenshots_dir, f"{tid}.png")
                await page.screenshot(path=shot, full_page=True)
            duration = time.time() - start
            results.append({
                "id": tid,"description": desc,"status": status,"error": error,"duration": duration
            })
        await browser.close()
    return results

def run(url, tests):
    return asyncio.run(run_tests(url, tests))
