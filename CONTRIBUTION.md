# Contribution Guide

## Overview

**PyTodo** is a simple Todo application built with a **FastAPI** backend (Python) and a **React** frontend (JavaScript). The backend stores data in‑memory and exposes CRUD endpoints for todo lists and their items. The frontend consumes these endpoints via **axios** and displays the lists.

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Backend | Python 3 (≥3.9) | – |
|         | FastAPI | 0.104.1 |
|         | Uvicorn (ASGI server) | 0.24.0 |
|         | Pydantic | 2.5.2 |
| Frontend | React (Create‑React‑App) | 18.3.1 |
|          | Axios | 1.7.2 |
|          | ESLint | 9.34.0 |
| Build / Dev Tools | npm | 8.19.3 |
|          | react‑scripts | 5.0.1 |

## Getting Started

### Prerequisites

- **Python** (>=3.9) and `pip`.
- **Node.js** (>=14) and `npm`.
- (Optional) Virtual environment for Python (`python -m venv .venv`).

### Backend Setup

```bash
# Clone the repo (if not already done)
git clone <repo-url>
cd pytodo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload
```

The API docs are available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

```bash
cd pytodo-frontend
npm install
npm start
```

The React app runs on `http://localhost:3000` and proxies API requests to the backend (see `package.json` proxy field).

### Running Tests

Backend: No tests are currently defined – feel free to add `pytest` suites.

Frontend:

```bash
npm test
```

### Building for Production

```bash
npm run build   # creates static assets in build/
# Deploy the `build` directory with any static server of your choice.
```

## Code Style & Linting

- **Python**: Follow PEP 8. The project uses `ruff` for linting (install with `pip install ruff`). Run `ruff check .`.
- **JavaScript/React**: ESLint configuration lives in `pytodo-frontend/.eslintrc.js`. Run `npm run lint`.

## Contribution Process

1. **Fork the repository** and clone your fork.
2. Create a **feature branch**: `git checkout -b feat/<description>`.
3. Make your changes, ensuring they adhere to the style guidelines above.
4. Add or update tests where applicable.
5. Run the full test suite and linters.
6. Commit with a clear message (use imperative mood, e.g., "Add UI for creating a new list").
7. Push to your fork and open a **Pull Request** against the `main` branch.

### Suggested Areas for Contribution

- **Backend**: Implement proper persistence (e.g., SQLite), add API versioning (`/v1/`), improve error handling, write unit tests.
- **Frontend**: Fix the current syntax errors, implement UI for adding/deleting/updating lists and items, align data shapes with the backend, add component tests.
- **Documentation**: Expand this guide, add screenshots, improve README.

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.
