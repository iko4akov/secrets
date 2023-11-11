from datetime import datetime


def format_date_time(day: int or str) -> str:
    """
    Takes an integer or string 'day' as an offset and
    returns a formatted string representing a future date and
    time based on the current date and time.
    Parameters:
        - day (int or str): The number of days to add to
        the current date. Can be an integer or a string.
    Returns:
    - str: A string representing the formatted future date and
    time in the format 'YYYY-MM-DD HH:MM'.
    """
    new_datetime = datetime(
        year=datetime.now().year,
        month=datetime.now().month,
        day=int(datetime.now().day) + int(day),
        hour=datetime.now().hour,
        minute=datetime.now().minute,
    )
    format_date = new_datetime.strftime('%Y-%m-%d %H:%M')
    return format_date
