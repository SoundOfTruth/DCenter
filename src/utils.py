from datetime import datetime

from flask import flash


def flash_pydantic_errors(errors):
    for error_data in errors:
        error_message = str(error_data.get("msg", "Непредвиденная ошибка"))
        flash(error_message, "error")


def get_date(date: datetime):
    return datetime.strftime(date, "%d.%m")
