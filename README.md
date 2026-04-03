<div align="center">

# 🧪 SauceDemo Playwright Test Automation

**Automated tests for [SauceDemo](https://www.saucedemo.com/) using Playwright + pytest + Python**

[![SauceDemo Playwright Tests](https://github.com/nikitabargat/saucedemo-playwright-tests/actions/workflows/test.yml/badge.svg)](https://github.com/nikitabargat/saucedemo-playwright-tests/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.58-2EAD33?logo=playwright&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.0-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Test Coverage](#-test-coverage)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Docker Support](#-docker-support)
- [Allure Reporting](#-allure-reporting)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Configuration](#-configuration)
- [License](#-license)

---

## 🎯 Overview

A practical test automation framework for the SauceDemo e-commerce demo site. Built using the Page Object Model pattern with Playwright for browser automation.

**What it covers:**
- ✅ Login scenarios (valid, invalid, locked user, empty fields)
- ✅ Product listing & sorting
- ✅ Product detail page
- ✅ Shopping cart operations
- ✅ Complete checkout flow (end-to-end)
- ✅ Navigation, menu, and logout
- ✅ Cross-browser testing (Chromium & Firefox)
- ✅ Allure reports with auto-captured failure screenshots

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **Playwright** | Browser automation |
| **pytest** | Test runner & assertions |
| **Allure Report** | HTML test reporting |
| **GitHub Actions** | CI/CD pipeline |
| **Docker** | Containerized test runs |
| **python-dotenv** | Environment config |

---

## 📁 Project Structure

```
saucedemo-playwright-tests/
├── .github/workflows/
│   └── test.yml                  # CI pipeline
├── config/
│   └── settings.py               # Centralized config (env vars)
├── pages/                        # Page Object Model
│   ├── base_page.py              # Shared Playwright helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   ├── checkout_step_one_page.py
│   ├── checkout_step_two_page.py
│   └── checkout_complete_page.py
├── tests/
│   ├── conftest.py               # Shared fixtures (page objects, logged-in session)
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_product_detail.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_navigation.py
├── utils/
│   └── helpers.py                # Test data loaders
├── test_data/
│   └── users.json                # Test credentials & product data
├── conftest.py                   # Root conftest (Allure screenshot hook)
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ✅ Test Coverage

| Module | Tests | What's Covered |
|---|:---:|---|
| 🔐 Login | 8 | Valid login, locked user, invalid password, empty fields, error dismissal |
| 📦 Inventory | 8 | Product count, sorting (A→Z, Z→A, price low/high), add/remove from cart |
| 🔍 Product Detail | 4 | Navigation to detail, content checks, add to cart, back button |
| 🛒 Cart | 5 | Items display, removal, persistence across navigation, badge count |
| 💳 Checkout | 7 | End-to-end purchase, form validation (3 fields), order summary, cancel |
| 🧭 Navigation | 5 | Header/footer, hamburger menu links, logout, about link, reset state |
| | **37** | |

### Running by Marker

```bash
pytest -m smoke              # Critical happy-path tests
pytest -m regression         # Full regression
pytest -m login              # Only login tests
pytest -m checkout           # Only checkout tests
pytest -m negative           # Negative scenarios
pytest -m e2e                # End-to-end flows
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Git**
- (Optional) **Docker** for containerized runs
- (Optional) **Allure CLI** to view reports locally

### Installation

```bash
# Clone the repo
git clone https://github.com/nikitabargat/saucedemo-playwright-tests.git
cd saucedemo-playwright-tests

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium firefox
```

### Environment Setup (Optional)

```bash
cp .env.example .env
# Edit .env if you want to change defaults (BASE_URL, HEADLESS, etc.)
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_login.py

# Run by marker
pytest -m smoke
pytest -m "login and negative"

# Run on Firefox
pytest --browser firefox

# Run headed (see the browser)
pytest --headed

# Run with slow motion for debugging
pytest --headed --slowmo 500
```

---

## 🐳 Docker Support

```bash
# Build and run
docker build -t saucedemo-tests .
docker run --rm saucedemo-tests

# Run on Firefox
docker run --rm saucedemo-tests pytest --browser firefox --alluredir=allure-results -v

# Run smoke tests only
docker run --rm saucedemo-tests pytest -m smoke --alluredir=allure-results -v

# Docker Compose — run both browsers at once
docker compose up --build
```

Allure results are volume-mounted to `./allure-results/` (Chromium) and `./allure-results-firefox/` (Firefox).

---

## 📊 Allure Reporting

After running tests, the `allure-results/` directory is created automatically.

### View the report

```bash
allure serve allure-results
```

This opens an interactive HTML report in your browser with:
- 📸 Screenshots attached on test failure
- 🏷️ Tests grouped by Feature / Story
- ⚠️ Severity levels (Blocker, Critical, Normal, Minor)
- 📝 Step-by-step execution details

### Install Allure CLI

```bash
# macOS
brew install allure

# Windows (Scoop)
scoop install allure

# Linux (apt)
sudo apt-get install allure
```

---

## ⚙️ CI/CD Pipeline

GitHub Actions workflow runs on every push to `main`/`master` and on pull requests.

**What it does:**
- Runs tests on **Chromium** and **Firefox** in parallel (matrix strategy)
- Uploads **Allure results** as artifacts (30-day retention)
- Uploads **failure screenshots** if any test fails

You can also trigger it manually via `workflow_dispatch`.

---

## 🔧 Configuration

Settings can be configured via environment variables or a `.env` file:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com` | Target URL |
| `HEADLESS` | `true` | Run headless |
| `BROWSER` | `chromium` | Browser engine |
| `DEFAULT_TIMEOUT` | `30000` | Wait timeout in ms |
| `SLOW_MO` | `0` | Slow-motion delay in ms |

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
