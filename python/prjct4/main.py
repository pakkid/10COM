from datetime import datetime

birth_year = int(input("Enter the year you were born: "))
birth_month = int(input("Enter the month you were born (1-12): "))
birth_day = int(input("Enter the day you were born: "))

current_date = datetime.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

years_old = current_year - birth_year
if current_month < birth_month or (current_month == birth_month and current_day < birth_day):
    years_old -= 1
    
total_months = (current_year - birth_year) * 12 + (current_month - birth_month)
if current_day < birth_day:
    total_months -= 1
birth_date = datetime(birth_year, birth_month, birth_day)
days_alive = (current_date - birth_date).days

this_year_birthday = datetime(current_year, birth_month, birth_day)
if this_year_birthday < current_date:
    next_birthday = datetime(current_year + 1, birth_month, birth_day)
else:
    next_birthday = this_year_birthday
days_until_birthday = (next_birthday - current_date).days

print(f"You are approximately {years_old} years old.")
print(f"You are approximately {total_months} months old.")
print(f"You are approximately {days_alive} days old.")
print(f"There are {days_until_birthday} days until your next birthday.")