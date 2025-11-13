# Employee Payroll Management System

End-to-end HR & Payroll platform built with FastAPI, MongoDB, React, Tailwind, and shadcn/ui.

## Features (MVP)
- HR Management: employees CRUD; attendance, leaves, reimbursements (coming next)
- Reports & Insights: CSV export endpoints (upcoming)
- One-click Payroll: mock payout provider (upcoming)
- Modern theme: dark/light toggle, animated landing page (frontend)

## Tech Stack
- Backend: FastAPI, Motor (MongoDB)
- Frontend: React + Vite + Tailwind + shadcn/ui

## Setup
1. Create `.env` from `.env.example` and set `MONGODB_URI` and `MONGODB_DB_NAME`.
2. Backend:
   - Create venv and install deps: `python -m venv .venv && .\\.venv\\Scripts\\activate && pip install -r backend/requirements.txt`
   - Run: `uvicorn backend.app.main:app --reload`
   - Visit: `http://localhost:8000/health` and `http://localhost:8000/docs`
3. Frontend (to be added next): initialize Vite React app with Tailwind and shadcn/ui.

## Environment Variables
- `MONGODB_URI`: your MongoDB connection string (keep credentials out of source control)
- `MONGODB_DB_NAME`: database name (default `payroll`)

## API (MVP)
- `GET /health`
- Employees:
  - `GET /api/v1/employees/`
  - `POST /api/v1/employees/`
  - `GET /api/v1/employees/{id}`
  - `PUT /api/v1/employees/{id}`
  - `DELETE /api/v1/employees/{id}`

## Development Notes
- Minimal dependencies are used intentionally. Charts/PDF generation planned for later.
- Future: authentication (email/Gmail), real payout providers, richer reports.

