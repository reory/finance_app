# 📌 Overview
![Last Commit](https://img.shields.io/github/last-commit/reory/finance_app?cacheSeconds=60)
![Repo Size](https://img.shields.io/github/repo-size/reory/finance_app?cacheSeconds=60)
![License](https://img.shields.io/badge/License-MIT-green)

![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge)

# 💰 SaaS FinanceApp

A modular, pipeline‑driven finance analytics SaaS built with Django & PostgreSQL

FinanceApp is a full‑stack personal finance analytics platform designed to ingest messy real‑world bank CSVs, clean and normalise the data, and present clear financial insights through dashboards, charts, and transaction management tools.

This is Version 1, focused on correctness, stability, modularity, and a clean user experience.
The architecture is intentionally scalable, with a dedicated ingestion pipeline, logging system, and multi‑app layout.

---

# 🚀 Key Features

<details>
  <summary>📸Screenshots</summary>

![Analytical Dashboard](screenshots/2.png)
![Main dashboard](screenshots/dashboard1.png)
![main dashboard](screenshots/dashboard2.png)
![main dashboard](screenshots/dashboard3.png)
![Running balance dashboard](screenshots/dashboard4.png)
![Main login dashboard](screenshots/login1.png)
![User profile dashboard](screenshots/profile1.png)
![CSV successfully cleaned dashboard](screenshots/testcsv1.png)
![Upload CSV dashboard](screenshots/uploadcsv1.png)
![Analytical Chart Dashboard](screenshots/chart1.png)

</details>

---

<details>
  <summary>📹Demo Video</summary>

[![Video of the dashboard]](demo.mp4)

</details>

---

# ⚙️ Tech Stack
- Django
- PostgreSQL
- Pytest
- Pydantic
- Modular multi‑app architecture

---

<details>
  <summary>🔐 Secure User Accounts (accounts app)</summary>

- User registration, login, logout

- Profile management

- Per‑user data isolation

- CSRF‑protected forms

- Redirect‑safe authentication flow

---

## 💸 Transaction Management (analytics app)
- Add, edit, delete transactions

- Category normalisation

- Clean currency formatting

- Paginated transaction list

- Per‑user transaction storage in PostgreSQL

---

## 📊 Dashboard & Analytics
- Monthly summaries

- Category totals

- Date‑range analytics

- Chart rendering (via chart.py)

- Clean UI templates for dashboards and charts

</details>

---

<details>
  <summary>📥 CSV Upload & Ingestion Pipeline</summary>

This is the heart of SaaS FinanceApp.
FinanceApp includes a two‑stage ingestion pipeline:

## 🧼 Stage 1 — CSVCleaner
A production‑grade cleaning engine that:

Handles messy CSV exports

Normalises dates into ISO format

Converts amounts into floats

Cleans categories (title‑case, typo fixes)

---

## 🏗️ Stage 2 — CSVImporter
A safe importer that:

- Accepts cleaned, validated rows

- Saves them to PostgreSQL

- Reports any remaining issues

- Guarantees no type errors or crashes

- Integrates with Django ORM cleanly

</details>

---

</details>
  <summary>🧱 Modular Architecture</summary>

The project is structured into multiple Django apps, each with a clear responsibility:

```
accounts/        → Authentication, profiles
apps/
  analytics/     → Transactions, dashboards, CSV ingestion
  logs/          → Logging system (analytics, pipeline, security)
  pipeline/      → Future pipeline engine (categorizer, cleaner, normalizer)
  uploads/       → Generic upload system (future expansion)
csv_data/        → Test CSVs
finance_app/     → Project-level config (settings, URLs, WSGI)
settings/        → Environment-specific settings (base/dev/prod)
templates/       → Global templates (login, register, base layout)
```

</details>

---

<details>
  <summary>🗄️ Database</summary>

```
FinanceApp uses PostgreSQL in development and production.
Environment variables (from .env):
DB_NAME=finance_app
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

---

## 🧩 Logging System (apps/logs/)
```
A dedicated logging subsystem with:
- analytics_logger.py
- pipeline_logger.py
- security_logger.py
- base.py

This allows:
- pipeline step logging
- error tracking
- security event logging
- analytics access logging
```

---

## 🧹 Example Cleaner Output
```
When uploading a messy CSV, the app might show:
Some rows were skipped during cleaning:
["Row 1: Invalid amount ' £2'",
 "Row 14: Invalid date format 'date'",
 "Row 15: Invalid amount '£2500'",
 "Row 35: Missing date"]
Valid rows are imported cleanly and appear in the dashboard.
```

</details>

---

# 🛠️ Installation

1. ## Clone the repo
```bash
git clone https://github.com/reory/finance_app.git
cd finance_app
```
2. ## Create a virtual environment
```bash
python -m venv venv
source venv/Scripts\activate # Windows
source venv\bin\activate  # Mac/Linux
```
3. ## Install dependencies
```bash
pip install -r requirements.txt
```
4. ## Configure environment variables
Create a .env file in the project root:

```bash
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=finance_app
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```
5. Run migrations
```bash
python manage.py migrate
```
6. Start the server
```bash
python manage.py runserver
```

--- 

<details>
  <summary>🎯 Version 1 Goals Achieved</summary>

- Modular Django architecture

- PostgreSQL-backed data storage

- Robust CSV ingestion pipeline

- Clean UI for transactions

- Dashboard analytics

- Logging system

- Authentication system

- Error‑tolerant CSV cleaning

This is a complete, functional SaaS foundation.

</details>

---

<details>
  <summary>🧪 Testing</summary>

This project includes a small, focused test suite that covers the critical paths of the backend:

- CSV Cleaner – validates incoming CSV rows and rejects invalid data

- CSV Importer – safely writes cleaned rows into the database

- Transaction Model – ensures the ORM model stores values correctly

- Schema & Field Validation – confirms required fields are present and correctly mapped

These tests ensure that the ingestion pipeline is stable, predictable, and safe to 
extend

▶️ Run the Pytest suite:
```bash
pytest -q
```

</details>

---

<details>
  <summary>🛣️ Roadmap</summary>

- [] Category inference

- [] Duplicate transaction detection

- [] Chart visualisations (Altair, Chart.js, or Plotly)

- [] Export to CSV

- [] Multi‑currency support

- [] Bank‑specific import presets

- [] Dashboard widgets

- [] API endpoints (REST or GraphQL)

- [] Background tasks (Celery or RQ)

</details>

---

<details>
  <summary>🏁 Final Notes</summary>

This app manages real‑world data, provides meaningful analytics, and is built with clean, maintainable Django architecture.

</details>

---

* **Built by Roy Peters** 😁
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Roy%20Peters-blue?logo=linkedin)](https://www.linkedin.com/in/roy-p-74980b382/)

