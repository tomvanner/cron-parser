ALLOWED_VALUES = {
    "minute": [i for i in range(0, 60)],
    "hour": [i for i in range(0, 24)],
    "day_of_month": [i for i in range(1, 32)],
    "month": [i for i in range(1, 13)],
    "day_of_week": [i for i in range(1, 8)]
}
ALLOWED_CHARS = {
    "minute": [",", "-", "*", "/"],
    "hour": [",", "-", "*", "/"],
    "day_of_month": [",", "-", "*", "?", "/", "W"],
    "month": [",", "-", "*", "/"],
    "day_of_week": [",", "-", "*", "?", "/"]
}
DAY_NAMES = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
MONTH_NAMES = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP","OCT",
    "NOV", "DEC"
]