# Project Overview

End‑to‑end Employee Payroll Management System for HR, with onboarding→exit, leave/attendance/reimbursements, reports/insights, and one‑click payroll processing. Modern dark/light theme and animated landing page. Guest access now, future Email/Gmail auth. Optimized for MongoDB.

## Tech Stack

* Backend: FastAPI, Python 3.11+, Motor (async MongoDB driver), Pydantic

* Database: MongoDB (Atlas/local) via `MONGODB_URI` in `.env` (username :amankumar1aiml2022\_db\_user and password : tck8qJB1aN6LzVwJ )

* Frontend: React 18 + TypeScript (Vite), Tailwind CSS, shadcn/ui (Radix)

* Testing: pytest, FastAPI TestClient; Vitest + React Testing Library

* Minimal deps: Native `fetch`, CSS keyframes; avoid heavy chart/PDF libs in MVP

## Monorepo Structure

* `backend/` FastAPI app

* `frontend/` React app

* `README.md` top‑level, updated per feature

* `.env` and `.env.example` (includes `MONGODB_URI`)

## Backend Design

* Layout: `app/main.py`, `app/api/v1/*`, `app/models/*` (Pydantic), `app/services/*`, `app/db/mongo.py`

* Config: `pydantic-settings` for env (e.g., `MONGODB_URI`, payout provider)

* DB Access: `motor.motor_asyncio.AsyncIOMotorClient` with per‑collection repositories

* Collections (Mongo):

  * `employees`, `departments`, `roles`, `contracts`

  * `attendance`, `leave_types`, `leave_requests`

  * `reimbursements`, `bank_accounts`

  * `payroll_runs`, `payroll_items`, `payslips`

  * `audit_logs`

* ID strategy: Use Mongo `ObjectId` serialized as string in API; references by storing related IDs

* Aggregations: Reporting via Mongo aggregation pipelines (group, sum, match)

* Payouts: Provider abstraction with `MockBankProvider`

## Frontend Design

* Routes:

  * `/` Animated landing

  * `/hr/employees`, `/hr/attendance`, `/hr/leaves`, `/hr/reimbursements`

  * `/payroll/run`, `/payroll/payslips`

  * `/reports`

  * `/settings` (theme toggle; future auth)

* Components: shadcn/ui (button, card, table, dialog, dropdown‑menu, input, textarea, select, tabs, sheet, toast, form, badge)

* Theming: system + toggle, stored in `localStorage`

## Data Model (Mongo)

* `Employee`: `_id:ObjectId`, name, email, phone, department\_id, role\_id, doj, status, base\_salary, bank\_account\_id

* `Department`: `_id`, name

* `Role`: `_id`, name

* `Contract`: `_id`, employee\_id, type, start\_date, end\_date, terms

* `Attendance`: `_id`, employee\_id, date, check\_in, check\_out, hours

* `LeaveType`: `_id`, name, accrual\_rule

* `LeaveRequest`: `_id`, employee\_id, type\_id, start\_date, end\_date, status, reason

* `Reimbursement`: `_id`, employee\_id, category, amount, date, status, note

* `BankAccount`: `_id`, employee\_id, masked\_account\_no, ifsc/swift, bank\_name

* `PayrollRun`: `_id`, period\_start, period\_end, status, processed\_at

* `PayrollItem`: `_id`, payroll\_run\_id, employee\_id, gross, deductions, reimbursements, net, payout\_ref

* `Payslip`: `_id`, payroll\_item\_id, html\_snapshot, generated\_at

* `AuditLog`: `_id`, actor, action, entity, entity\_id, timestamp

## API Surface (v1)

* `GET /health`

* Employees: `GET/POST/PUT/DELETE /api/v1/employees`, `GET /api/v1/employees/{id}`

* Attendance: `GET/POST /api/v1/attendance`, `GET /api/v1/attendance?employee_id&from&to`, `POST /api/v1/attendance/import` (CSV)

* Leave: `GET/POST /api/v1/leaves`, `PUT /api/v1/leaves/{id}`; types: `GET/POST /api/v1/leave-types`

* Reimbursements: `GET/POST /api/v1/reimbursements`, `PUT /api/v1/reimbursements/{id}`

* Payroll: `POST /api/v1/payroll/run` (compute items), `POST /api/v1/payroll/payout` (mock), `GET /api/v1/payslips?run_id`

* Reports: `GET /api/v1/reports/payroll`, `GET /api/v1/reports/attendance`, `GET /api/v1/reports/reimbursements`, `GET /api/v1/reports/export.csv?type=...`

## Payroll Flow (Mongo‑optimized)

1. Select period and employees
2. Aggregate attendance (`$match` by date, `$group` by employee) to compute prorations
3. Compute gross/net per employee, include approved reimbursements (`$match` + `$group`)
4. Insert `payroll_run` and `payroll_items` in batch
5. Generate payslip HTML snapshot stored with `payslips`
6. One‑click payout with mock provider; update `payout_ref` in items and audit log

## Reports & Insights (Aggregation)

* Payroll: totals per period/department using `$lookup` (or store department\_id on employee), `$group`

* Attendance: totals/hours by employee and date range

* Reimbursements: totals by category/month

* Exports: server generates CSV from aggregation cursors

## Theming & UX

* Dark/light theme with toggle and system preference

* Animated landing (CSS keyframes, scroll reveal)

* Cross‑linked views: employee → attendance/leaves/payroll history

## Testing & Quality

* Backend: pytest + TestClient; use `mongomock` or a test database URI

* Frontend: Vitest + Testing Library

* Linting/formatting: `ruff`, `eslint` + `prettier`

## Dev Setup (Commands)

* Backend

  * `python -m venv .venv && .\.venv\Scripts\activate`

  * `pip install fastapi uvicorn[standard] motor pydantic pydantic-settings python-multipart`

  * Set `.env`: `MONGODB_URI=mongodb+srv://<username>:<password>@<host>/<db>?retryWrites=true&w=majority`

  * `uvicorn app.main:app --reload`

* Frontend

  * `npm create vite@latest frontend -- --template react-ts`

  * `cd frontend && npm i && npm i -D tailwindcss postcss autoprefixer`

  * `npx tailwindcss init -p` and configure `tailwind.config.js`

  * Initialize shadcn/ui and add core components

  * `npm run dev`

## Git Commit Plan (Incremental)

1. Scaffold monorepo (backend+frontend), README, healthcheck
2. MongoDB client setup, repositories, env config
3. Employees CRUD API
4. Attendance API + CSV import
5. Leave API + approvals + leave types
6. Reimbursements API
7. Payroll engine (compute, items, payslip HTML) + payout mock
8. Reports endpoints + CSV export (aggregation pipelines)
9. Frontend setup (Tailwind, shadcn, theming)
10. Animated landing page
11. HR pages (employees, attendance, leaves, reimbursements)
12. Payroll pages (run, payslips, payout)
13. Reports pages and tables
14. Print/export payslip from HTML (browser print)
15. Polish, cross‑links, toasts, validations
16. README updates and final usage docs

## README Maintenance

* Document env vars (including `MONGODB_URI`), setup steps, endpoints, routes

* Update feature list and screenshots per commit

## Future Extensions

* Auth: email/password + Google OAuth; roles/permissions

* Real payouts: provider integration and webhooks

* Charts: lightweight SVG charts or small chart lib if needed

* Server‑side PDF later if desired

* Multi‑tenant support via `org_id` on documents

## Assumptions

* You will supply `MONGODB_URI` with your username in `.env`

* Payment remains mocked in MVP; no real bank transfers

* Minimal dependencies maintained throughout

