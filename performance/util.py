from datetime import date
import calendar

def is_month_completed(month: int, year: int) -> bool:
    """
    Return True if the given month/year is fully completed.
    Example: February 2026 is completed only after Feb 28/29, 2026.
    """
    today = date.today()

    # last day of that month
    last_day = calendar.monthrange(year, month)[1]
    last_date = date(year, month, last_day)

    return today > last_date