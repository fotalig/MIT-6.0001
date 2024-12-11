

annual_salary = int(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = int(input('Enter cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal: '))

# annual_salary = 75000
# portion_saved = .05
# total_cost = 1500000
# semi_annual_raise = 0.05
portion_down_payment = 0.25
current_savings = 0
r = 0.04

n_months = 0

while current_savings <= total_cost*portion_down_payment:
    current_savings += current_savings*r/12 + annual_salary*portion_saved/12
    n_months += 1
    if not bool(n_months % 6):
        annual_salary *= (1+semi_annual_raise)

print('Numer of months', n_months)
