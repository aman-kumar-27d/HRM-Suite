import asyncio
from datetime import datetime


async def aggregate_attendance(db, start: str, end: str):
    pipeline = [
        {"$match": {"date": {"$gte": start, "$lte": end}}},
        {"$group": {"_id": "$employee_id", "hours": {"$sum": {"$ifNull": ["$hours", 0]}}}},
    ]
    result = await asyncio.to_thread(lambda: list(db.attendance.aggregate(pipeline)))
    return {str(doc["_id"]): float(doc.get("hours", 0)) for doc in result}


async def aggregate_reimbursements(db, start: str, end: str):
    pipeline = [
        {"$match": {"date": {"$gte": start, "$lte": end}, "status": "approved"}},
        {"$group": {"_id": "$employee_id", "amount": {"$sum": "$amount"}}},
    ]
    result = await asyncio.to_thread(lambda: list(db.reimbursements.aggregate(pipeline)))
    return {str(doc["_id"]): float(doc.get("amount", 0)) for doc in result}


async def compute_payroll_items(db, start: str, end: str):
    attendance_hours = await aggregate_attendance(db, start, end)
    reimburse = await aggregate_reimbursements(db, start, end)
    employees = await asyncio.to_thread(lambda: list(db.employees.find({"status": "active"})))
    items = []
    for emp in employees:
        emp_id = str(emp["_id"]) if "_id" in emp else emp.get("id")
        base = float(emp.get("base_salary", 0) or 0)
        hours = float(attendance_hours.get(emp_id, 0))
        hourly_rate = base / 160 if base else 0
        gross = round(base + hourly_rate * max(0, hours - 160), 2)
        deductions = round(base * 0.05, 2) if base else 0
        reimb = round(reimburse.get(emp_id, 0), 2)
        net = round(gross - deductions + reimb, 2)
        items.append({
            "employee_id": emp_id,
            "gross": gross,
            "deductions": deductions,
            "reimbursements": reimb,
            "net": net,
        })
    return items


def generate_payslip_html(item, employee):
    return f"""
    <html><body>
    <h2>Payslip</h2>
    <p>Employee: {employee.get('name')}</p>
    <p>Gross: {item['gross']}</p>
    <p>Deductions: {item['deductions']}</p>
    <p>Reimbursements: {item['reimbursements']}</p>
    <p>Net: {item['net']}</p>
    <small>Generated at {datetime.utcnow().isoformat()}Z</small>
    </body></html>
    """

