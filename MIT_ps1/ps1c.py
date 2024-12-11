

# annual_salary = int(input('Enter your annual salary: '))
# portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))

annual_salary_init = 300000
annual_salary = annual_salary_init
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25
current_savings = 0
r = 0.04

epsilon = 100
n_iter = 0

n_months = 36

portion_saved_low = int(0)
portion_saved_high = int(10000)

portion_saved = (portion_saved_high + portion_saved_low) // 2

portion_saved_prev = 0
max_check = False

while abs(current_savings - total_cost*portion_down_payment) > epsilon:

    current_savings = 0.0
    annual_salary = annual_salary_init

    for current_month in range(n_months+1):
        portion_saved_decimal = portion_saved/10000
        current_savings += current_savings*r/12 + annual_salary*portion_saved_decimal/12
        if not bool(current_month % 6):
            annual_salary *= (1+semi_annual_raise)

    # print(current_savings)

    if current_savings < total_cost*portion_down_payment:
        portion_saved_low = portion_saved
    elif current_savings > total_cost*portion_down_payment:
        portion_saved_high = portion_saved
    portion_saved = (portion_saved_high + portion_saved_low) // 2
    # print(portion_saved)
    if portion_saved == portion_saved_prev:
        print("It is not possible to pay the down payment in three years")
        max_check = True
        break

    portion_saved_prev = portion_saved
    n_iter += 1
if not max_check:
    print(current_savings)
    print("Best savings rate: ", portion_saved/10000*100, "%")
    print("Number of iterations ", n_iter)
