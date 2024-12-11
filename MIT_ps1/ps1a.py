

annual_salary = int(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = int(input('Enter cost of your dream home: '))
portion_down_payment = 0.25
current_savings = 0
r = 0.04

n_months = 0

while current_savings <= total_cost*portion_down_payment:
    current_savings += current_savings*r/12 + annual_salary*portion_saved/12
    n_months += 1

print('Numer of months', n_months)
