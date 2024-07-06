from datetime import datetime
today = datetime(2024, 7, 6)
target_date = datetime(2050, 1, 28)
days_difference = (target_date - today).days
print(days_difference)