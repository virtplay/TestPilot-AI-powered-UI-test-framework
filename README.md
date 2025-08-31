# TestPilot-AI-powered-UI-test-framework
analyzes a page,  generates test cases using an LLM,  runs them automatically with Playwright,  and produces a clear report.

**TestPilot** 🚀
This will include **intro, features, requirements, installation, Ollama setup, Playwright setup, and usage guide**.

Here’s a first draft:

````markdown
# 🛠️ TestPilot – AI-Powered UI Test Framework

TestPilot is an **AI-driven UI testing framework** that:  
- 🔍 Analyzes any given webpage with **Playwright**  
- 🤖 Generates test cases automatically using **Ollama (open-source LLM)**  
- ▶️ Executes tests in the browser  
- 📊 Produces clean, human-readable HTML reports  

---

## ✨ Features
- Automatic **UI element discovery** (inputs, buttons, checkboxes, etc.)
- AI-powered **test case generation**
- Executes tests via **Playwright**
- **HTML reports** with pass/fail status
- Works **locally** with no external cloud dependency
- Uses **Ollama** → free & open-source LLM backend

---

## 📋 Requirements
- macOS / Linux (Windows WSL2 also works)
- **Python**: `3.11` or `3.12`  
- **Playwright**: `1.38.0`  
- **Ollama**: latest stable (tested with `ollama 0.1.30+`)  
- Virtual environment recommended  

---

## ⚡ Installation

### 1. Clone the Repo
```bash
git clone https://github.com/<your-username>/testpilot.git
cd testpilot
````

### 2. Setup Python Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate   # macOS/Linux
# On Windows (PowerShell)
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

---

## 🤖 Ollama Setup

1. Install **Ollama** (macOS/Linux):
   👉 [https://ollama.ai/download](https://ollama.ai/download)

2. Verify installation:

```bash
ollama --version
```

3. Pull a small model (fast for local testing):

```bash
ollama pull smollm2:135m
```

4. Or use a larger model for better results:

```bash
ollama pull llama3:8b
```

---

## ▶️ Usage

### Run on any website

```bash
./examples/sample_run.sh https://httpbin.org/forms/post
```

This will:

1. Analyze the page (`analyzer.py`)
2. Generate tests (`test_generator.py`)
3. Run tests (`runner.py`)
4. Produce a report in `results/ai_ui_test_report.html`

### Example Output

```
Analyzed page: https://httpbin.org/forms/post
Detected 11 actions
Generated 11 tests
Report created: results/ai_ui_test_report.html
```

Open the HTML file in a browser to see the results ✅

---

## 📊 Sample Report

![Sample Report](docs/sample_report.png)

---

## 🔧 Configuration

* Default Ollama model: `smollm2:135m`
* Change model by editing `sample_run.sh`:

```bash
MODEL="llama3:8b"
```

---

## 🧩 Project Structure

```
.
├── analyzer.py        # Analyzes webpage with Playwright
├── test_generator.py  # Generates test cases via Ollama
├── runner.py          # Executes tests
├── report.py          # Generates HTML reports
├── examples/          # Sample run scripts
├── results/           # Test reports
└── requirements.txt   # Python dependencies
```

---

## 📜 License

MIT License © 2025 Karthik Bs

---

## 🙌 Credits

* [Playwright](https://playwright.dev/) for browser automation
* [Ollama](https://ollama.ai/) for local LLM test generation
* Built with ❤️ by **Karthik Bs**

```

---

✅ This README covers everything: Python version, Playwright version, Ollama setup, installation steps, usage, and project structure.  

Do you want me to also **generate the README.md file into your repo folder** so you can directly open it?
```
