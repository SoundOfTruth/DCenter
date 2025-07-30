import datetime
import calendar
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.database.core import session_factory # noqa
from src.models import Appointment, Doctor # noqa


def add_appointments(session: Session):
    doctors = session.scalars(select(Doctor)).all()
    current_date = datetime.date.today()
    _, last_month_day = calendar.monthrange(
        current_date.year, current_date.month
    )
    for doctor in doctors:
        working_start_time = datetime.time(10, 00)
        working_end_time = datetime.time(18, 00)
        appointment_delta = datetime.timedelta(minutes=30)

        for day in range(current_date.day, last_month_day + 1):
            date = datetime.date(current_date.year, current_date.month, day)
            time = working_start_time
            timestemp = datetime.datetime.combine(date, time)
            while timestemp.time() <= working_end_time:
                appointement = Appointment(date=timestemp, doctor_id=doctor.id)
                session.add(appointement)
                timestemp += appointment_delta


if __name__ == "__main__":
    with session_factory() as session:
        try:
            add_appointments(session)
            session.commit()
            print("appointments inserted")
        except IntegrityError:
            session.rollback()
            raise Exception("data insert failed")
