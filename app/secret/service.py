from datetime import datetime


def format_date_time(day: int) -> str:
    new_datetime = datetime(
        year=datetime.now().year,
        month=datetime.now().month,
        day=int(datetime.now().day) + int(day),
        hour=datetime.now().hour,
        minute=datetime.now().minute,
    )
    format_date = new_datetime.strftime('%Y-%m-%d %H:%M')
    return format_date
