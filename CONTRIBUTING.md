# Contributing to FinanceApp

Thank you for your interest in contributing to FinanceApp!
This project is intentionally modular and clean, so contributions should follow a few simple guidelines to keep the codebase consistent and maintainable.

---

# 🧱 Project Principles

Keep code modular — each app has a clear responsibility.

Maintain clean, readable Python and Django conventions.

Prioritise data safety and pipeline stability.

Write tests only for critical paths, not everything.

---

# 🛠️ How to Contribute
1. ## Fork & Clone
```bash
git clone https://github.com/reory/finance_app.git
```

---

2. ## Create a Feature Branch
```bash
git checkout -b feature/my-improvement
```

---

3. ## Follow Code Style

- Use clear naming and small, focused functions.

- Keep imports tidy and avoid unused code.

- Place new logic in the correct Django app.

---

4. ## Add Tests (Only Where Needed)
If your change affects:

- CSV cleaning

- Importing

- Transaction model

- Authentication
…then add or update a test.

Run the suite:

```bash
pytest -q
```

---

5. ## Submit a Pull Request
Include:

- A short description of the change

- Why it improves the project

- Any notes for reviewers

---

# Thank you for viewing my project. Happy coding! 😁