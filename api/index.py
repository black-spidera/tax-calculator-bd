from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    gender: str = Form(...),
    marital_status: str = Form(...),
    age: int = Form(...),
    salary1: float = Form(...),
    salary2: float = Form(...),
    bonus: float = Form(...),
    freelance: float = Form(...),
    rental: float = Form(...),
    other: float = Form(...),
    rent: float = Form(...),
    life: float = Form(...),
    nsc: float = Form(...),
    dps: float = Form(...),
    mutual: float = Form(...),
    donation: float = Form(...),
    energy: float = Form(...),
    computer: float = Form(...),
    conveyance: float = Form(...),
    medical: float = Form(...)
):
    income_salary = salary1 * 7 + salary2 * 5
    gross_income = income_salary + bonus + freelance + rental + other

    rent_rebate = min(0.5 * rent * 12, 25000)
    rebate_eligible = sum([rent_rebate, life, nsc, dps, mutual, donation, energy, computer])
    rebate_eligible = min(rebate_eligible, gross_income * 0.25)
    rebate = rebate_eligible * 0.15

    # Convert monthly conveyance and medical to yearly
    conveyance_yearly = conveyance * 12
    medical_yearly = medical * 12

    taxable_income = gross_income - (conveyance_yearly + medical_yearly)

    # Slab based on gender/marital/age
    if age >= 65:
        slab_0 = 450000
    elif gender == "female" or marital_status == "married":
        slab_0 = 400000
    else:
        slab_0 = 350000

    slab_1 = 100000
    slab_2 = 300000

    if taxable_income <= slab_0:
        tax = 0
    elif taxable_income <= slab_0 + slab_1:
        tax = (taxable_income - slab_0) * 0.05
    elif taxable_income <= slab_0 + slab_1 + slab_2:
        tax = slab_1 * 0.05 + (taxable_income - slab_0 - slab_1) * 0.10
    else:
        tax = slab_1 * 0.05 + slab_2 * 0.10 + (taxable_income - slab_0 - slab_1 - slab_2) * 0.15

    tax_final = max(0, tax - rebate)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "gross": f"{gross_income:,.2f}",
        "taxable": f"{taxable_income:,.2f}",
        "rebate": f"{rebate:,.2f}",
        "tax_before": f"{tax:,.2f}",
        "tax_after": f"{tax_final:,.2f}"
    })
