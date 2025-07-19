def get_float_input(prompt, example=0):
    while True:
        try:
            value = float(input(f"{prompt} (e.g. {example}): "))
            if value < 0:
                print("❌ Negative value not allowed, try again.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def get_choice_input(prompt, choices):
    choices_str = "/".join(choices)
    while True:
        value = input(f"{prompt} ({choices_str}): ").strip().lower()
        if value in choices:
            return value
        else:
            print(f"❌ Invalid choice. Choose one of: {choices_str}")

def calculate_tax_slabs(taxable_income, gender, marital_status, age):
    # FY 2024-25 slabs for Bangladesh, different for male/female/senior/married

    # Define slabs (amounts in BDT)
    # The slabs below are typical; you can update if govt changes
    if age >= 65:  # Senior citizen slab (male/female)
        slab_0 = 450000  # 0% tax
        slab_1 = 100000  # 5%
        slab_2 = 300000  # 10%
    elif gender == "female" or marital_status == "married":
        slab_0 = 400000
        slab_1 = 100000
        slab_2 = 300000
    else:  # male unmarried or others
        slab_0 = 350000
        slab_1 = 100000
        slab_2 = 300000

    tax = 0
    if taxable_income <= slab_0:
        tax = 0
    elif taxable_income <= slab_0 + slab_1:
        tax = (taxable_income - slab_0) * 0.05
    elif taxable_income <= slab_0 + slab_1 + slab_2:
        tax = slab_1 * 0.05 + (taxable_income - slab_0 - slab_1) * 0.10
    else:
        # Beyond slab 2, 15% tax
        tax = slab_1 * 0.05 + slab_2 * 0.10 + (taxable_income - slab_0 - slab_1 - slab_2) * 0.15

    return tax

def main():
    print("🧾 Bangladesh Income Tax Calculator (FY 2024–25)\n")

    # Personal info
    gender = get_choice_input("Enter gender", ["male", "female"])
    marital_status = get_choice_input("Marital status", ["single", "married"])
    age = int(get_float_input("Enter your age (years)", 30))

    # Income sources
    print("\n💰 Enter your income details:")
    salary_monthly_1 = get_float_input("Monthly salary (period 1 months)")
    period_1_months = int(get_float_input("Number of months for period 1", 6))
    salary_monthly_2 = get_float_input("Monthly salary (period 2 months)")
    period_2_months = int(get_float_input("Number of months for period 2", 6))
    freelance_income = get_float_input("Freelance income total in BDT (if none, 0)", 0)
    rental_income = get_float_input("Rental income total in BDT (if none, 0)", 0)
    other_income = get_float_input("Other income (dividends, interest, etc.)", 0)
    bonus = get_float_input("Total yearly bonus in BDT", 0)

    # Total income
    total_salary_income = salary_monthly_1 * period_1_months + salary_monthly_2 * period_2_months
    gross_income = total_salary_income + freelance_income + rental_income + other_income + bonus
    print(f"\n📌 Total Gross Income: ৳{gross_income:.2f}")

    # Deductions and exemptions
    print("\n📉 Enter your deductions and rebate eligible investments:")

    # Tax rebate eligible investments (max 25% of gross income eligible for rebate)
    monthly_rent = get_float_input("Monthly house rent (max 50% eligible, capped at 25,000 yearly)", 16000)
    life_insurance = get_float_input("Yearly life insurance premium", 0)
    nsc = get_float_input("Investment in NSC", 0)
    dps = get_float_input("Yearly DPS or pension contribution", 0)
    mutual_fund = get_float_input("Investment in mutual funds / shares", 0)
    donation = get_float_input("Donation to govt. welfare or PM fund (with receipt)", 0)
    energy_devices = get_float_input("Energy-saving devices (fridge, fan, AC)", 0)
    computer_purchase = get_float_input("Computer/laptop purchase for education/profession", 0)

    # Other deductions
    conveyance = get_float_input("Yearly conveyance allowance (tax exempt)", 0)
    medical_allowance = get_float_input("Yearly medical allowance (tax exempt)", 0)

    # Calculate rebate eligible amount
    rent_rebate = min(0.5 * monthly_rent * 12, 25000)
    total_rebate_eligible = (
        rent_rebate + life_insurance + nsc + dps + mutual_fund +
        donation + energy_devices + computer_purchase
    )
    max_rebate_eligible = min(total_rebate_eligible, gross_income * 0.25)
    rebate_amount = max_rebate_eligible * 0.15

    # Calculate taxable income
    taxable_income = gross_income - (conveyance + medical_allowance)

    print(f"\n✅ Total rebate eligible investment: ৳{max_rebate_eligible:.2f}")
    print(f"✅ Tax rebate (15% of eligible investment): ৳{rebate_amount:.2f}")
    print(f"✅ Taxable income after exemptions (before rebate): ৳{taxable_income:.2f}")

    # Calculate tax using slabs
    tax_before_rebate = calculate_tax_slabs(taxable_income, gender, marital_status, age)
    tax_after_rebate = max(0, tax_before_rebate - rebate_amount)

    print("\n🧾 Tax Summary:")
    print(f"➡️ Tax before rebate: ৳{tax_before_rebate:.2f}")
    print(f"➡️ Tax rebate: ৳{rebate_amount:.2f}")
    print(f"📌 Final tax payable: ৳{tax_after_rebate:.2f}")

if __name__ == "__main__":
    main()
