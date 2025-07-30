
import json
import sys
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.database.core import session_factory # noqa
from src.models import Clinic, Doctor, Speciality, Service # noqa


def fill_clinics(session: Session):
    session.add_all([
        Clinic(address='ул. Лаптева 1'),
        Clinic(address='ул. Мира 1')
    ])
    session.flush()


def fill_specialities(session: Session):
    with open('data/specialities.json', 'r', encoding='utf-8') as f:
        specialities = json.load(f)
    for speciality in specialities:
        s = Speciality(name=speciality)
        session.add(s)
    session.flush()


def add_services(session: Session):
    with open('data/services.json', 'r', encoding='utf-8') as f:
        services = json.load(f)
    for i in range(len(services)):
        session.add(
            Service(
                name=services[i][0],
                price=services[i][1],
                speciality_id=services[i][2]
            )
        )


def add_doctors(session: Session):
    doctors = [
        Doctor(
            speciality_id=1,
            clinic_id=1,
            fullname="Смирнова Александра Александровна",
            qualification=(
                "Врач аллерголог-иммунолог высшей квалификационной категории"
            ),
            experience_start=2014
        ),
        Doctor(
            speciality_id=2,
            clinic_id=1,
            fullname="Иванов Иван Иванович",
            qualification=(
                "Врач вертебролог, "
                "мануальный терапевт первой квалификационной категории"
            ),
            experience_start=2003
        ),
        Doctor(
            speciality_id=3,
            clinic_id=1,
            fullname="Иванов Александр Иванович",
            qualification=(
                "Врач-гастроэнтеролог "
                "высшей квалификационной категории, кандидат медицинских наук"
            ),
            experience_start=2007
        ),
        Doctor(
            speciality_id=4,
            clinic_id=1,
            fullname="Иванов Илья Иванович",
            qualification="Врач-кардиолог высшей квалификационной категории",
            experience_start=2008
        ),
        Doctor(
            speciality_id=5,
            clinic_id=1,
            fullname="Иванов Сергей Иванович",
            qualification="Врач-невролог высшей квалификационной категории",
            experience_start=2001
        ),
        Doctor(
            speciality_id=6,
            clinic_id=1,
            fullname="Максимов Сергей Иванович",
            qualification=(
                "Врач-оториноларинголог высшей квалификационной категории"
            ),
            experience_start=2011
        ),
        Doctor(
            speciality_id=7,
            clinic_id=1,
            fullname="Кузнецова Ксения Викторовна",
            qualification="Врач-офтальмолог",
            experience_start=2001
        ),
        Doctor(
            speciality_id=8,
            clinic_id=1,
            fullname="Петрова Александра Викторовна",
            qualification="Врач-эндокринолог",
            experience_start=2014
        ),
        Doctor(
            speciality_id=1,
            clinic_id=2,
            fullname="Ануфриева Александра Александровна",
            qualification=(
                "Врач аллерголог-иммунолог высшей квалификационной категории"
            ),
            experience_start=2012
        ),
        Doctor(
            speciality_id=2,
            clinic_id=2,
            fullname="Петров Иван Иванович",
            qualification=(
                "Врач вертебролог, "
                "мануальный терапевт первой квалификационной категории"
            ),
            experience_start=2007
        ),
        Doctor(
            speciality_id=3,
            clinic_id=2,
            fullname="Иванов Петр Иванович",
            qualification=(
                "Врач-гастроэнтеролог "
                "высшей квалификационной категории, "
                "кандидат медицинских наук"
            ),
            experience_start=2001
        ),
        Doctor(
            speciality_id=4,
            clinic_id=2,
            fullname="Иванов Максим Иванович",
            qualification="Врач-кардиолог высшей квалификационной категории",
            experience_start=2002
        ),
        Doctor(
            speciality_id=5,
            clinic_id=2,
            fullname="Иванов Иван Иванович",
            qualification="Врач-невролог высшей квалификационной категории",
            experience_start=2004
        ),
        Doctor(
            speciality_id=6,
            clinic_id=2,
            fullname="Максимов Александр Иванович",
            qualification=(
                "Врач-оториноларинголог "
                "высшей квалификационной категории"
            ),
            experience_start=2005
        ),
        Doctor(
            speciality_id=7,
            clinic_id=2,
            fullname="Смирнова Ксения Викторовна",
            qualification="Врач-офтальмолог",
            experience_start=2003
        ),
        Doctor(
            speciality_id=8,
            clinic_id=2,
            fullname="Василенко Александра Викторовна",
            qualification="Врач-эндокринолог",
            experience_start=2015
        )
    ]
    session.add_all(doctors)


if __name__ == "__main__":
    with session_factory() as session:
        try:
            fill_clinics(session)
            fill_specialities(session)
            add_services(session)
            add_doctors(session)
            session.commit()
            print("base data inserted")
        except IntegrityError:
            session.rollback()
            raise Exception("data insert failed")
