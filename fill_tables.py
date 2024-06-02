from main import db, app, Clinics, Specialities, Doctors, Services, Appointment, Users
from data import services
from datetime import datetime, timedelta    


def fill_appointments():
    with app.app_context():
        for i in range(1, 17):
            for j in range(1, 8):
                a1 = Appointment(date=datetime(2024, 6, j, 15, 30), doctor_id=i)
                a2 = Appointment(date=datetime(2024, 6, j, 16, 00), doctor_id=i)
                a3 = Appointment(date=datetime(2024, 6, j, 16, 30), doctor_id=i)
                a4 = Appointment(date=datetime(2024, 6, j, 17, 00), doctor_id=i)
                a5 = Appointment(date=datetime(2024, 6, j, 17, 30), doctor_id=i)
                a6 = Appointment(date=datetime(2024, 6, j, 16, 00), doctor_id=i)
                db.session.add(a1)
                db.session.add(a2)
                db.session.add(a3)
                db.session.add(a4)
                db.session.add(a5)
                db.session.add(a6)
        db.session.commit()


def fill_clinics():
    with app.app_context():
        c1 = Clinics(name='ул. Лаптева 1')
        c2 = Clinics(name='ул. Мира 1')
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()


def fill_specialities():
    with app.app_context():
        f = open('specialities.txt', 'r', encoding="utf-8")
        specialities = f.read().split("\n")
        for speciality in specialities:
            s = Specialities(name=speciality)
            db.session.add(s)
        db.session.commit()
        f.close()


def fill_services():
    with app.app_context():
        for i in range(len(services)):
            s = Services(name=services[i][0], price=services[i][1], speciality_id=services[i][2])
            db.session.add(s)
        db.session.commit()


def fill_doctors():
    photo_url = "http://www.мырусымывместе.рф/tmpl/komanda/NoFoto(m).jpg"
    with app.app_context():
        d1 = Doctors(
            speciality_id=1,
            clinic_id=1,
            fullname="Смирнова Александра Александровна",
            qualification="Врач аллерголог-иммунолог высшей квалификационной категории",
            experience=2014,
            photo_url=photo_url
        )
        d2 = Doctors(
            speciality_id=2,
            clinic_id=1,
            fullname="Иванов Иван Иванович",
            qualification="Врач вертебролог, мануальный терапевт первой квалификационной категории",
            experience=2003,
            photo_url=photo_url
        )
        d3 = Doctors(
            speciality_id=3,
            clinic_id=1,
            fullname="Иванов Александр Иванович",
            qualification="Врач-гастроэнтеролог высшей квалификационной категории, кандидат медицинских наук",
            experience=2007,
            photo_url=photo_url
        )
        d4 = Doctors(
            speciality_id=4,
            clinic_id=1,
            fullname="Иванов Илья Иванович",
            qualification="Врач-кардиолог высшей квалификационной категории",
            experience=2008,
            photo_url=photo_url
        )
        d5 = Doctors(
            speciality_id=5,
            clinic_id=1,
            fullname="Иванов Сергей Иванович",
            qualification="Врач-невролог высшей квалификационной категории",
            experience=2001,
            photo_url=photo_url
        )
        d6 = Doctors(
            speciality_id=6,
            clinic_id=1,
            fullname="Максимов Сергей Иванович",
            qualification="Врач-оториноларинголог высшей квалификационной категории",
            experience=2011,
            photo_url=photo_url
        )
        d7 = Doctors(
            speciality_id=7,
            clinic_id=1,
            fullname="Кузнецова Ксения Викторовна",
            qualification="Врач-офтальмолог",
            experience=2001,
            photo_url=photo_url
        )
        d8 = Doctors(
            speciality_id=8,
            clinic_id=1,
            fullname="Петрова Александра Викторовна",
            qualification="Врач-эндокринолог",
            experience=2014,
            photo_url=photo_url
        )
        d9 = Doctors(
            speciality_id=1,
            clinic_id=2,
            fullname="Ануфриева Александра Александровна",
            qualification="Врач аллерголог-иммунолог высшей квалификационной категории",
            experience=2012,
            photo_url=photo_url
        )
        d10 = Doctors(
            speciality_id=2,
            clinic_id=2,
            fullname="Петров Иван Иванович",
            qualification="Врач вертебролог, мануальный терапевт первой квалификационной категории",
            experience=2007,
            photo_url=photo_url
        )
        d11 = Doctors(
            speciality_id=3,
            clinic_id=2,
            fullname="Иванов Петр Иванович",
            qualification="Врач-гастроэнтеролог высшей квалификационной категории, кандидат медицинских наук",
            experience=2001,
            photo_url=photo_url
        )
        d12 = Doctors(
            speciality_id=4,
            clinic_id=2,
            fullname="Иванов Максим Иванович",
            qualification="Врач-кардиолог высшей квалификационной категории",
            experience=2002,
            photo_url=photo_url
        )
        d13 = Doctors(
            speciality_id=5,
            clinic_id=2,
            fullname="Иванов Иван Иванович",
            qualification="Врач-невролог высшей квалификационной категории",
            experience=2004,
            photo_url=photo_url
        )
        d14 = Doctors(
            speciality_id=6,
            clinic_id=2,
            fullname="Максимов Александр Иванович",
            qualification="Врач-оториноларинголог высшей квалификационной категории",
            experience=2005,
            photo_url=photo_url
        )
        d15 = Doctors(
            speciality_id=7,
            clinic_id=2,
            fullname="Смирнова Ксения Викторовна",
            qualification="Врач-офтальмолог",
            experience=2003,
            photo_url=photo_url
        )
        d16 = Doctors(
            speciality_id=8,
            clinic_id=2,
            fullname="Василенко Александра Викторовна",
            qualification="Врач-эндокринолог",
            experience=2015,
            photo_url=photo_url
        )
        db.session.add(d1)
        db.session.add(d2)
        db.session.add(d3)
        db.session.add(d4)
        db.session.add(d5)
        db.session.add(d6)
        db.session.add(d7)
        db.session.add(d8)
        db.session.add(d9)
        db.session.add(d10)
        db.session.add(d11)
        db.session.add(d12)
        db.session.add(d13)
        db.session.add(d14)
        db.session.add(d15)
        db.session.add(d16)
        db.session.commit()


if __name__ == "__main__":
    fill_clinics()
    fill_specialities()
    fill_services()
    fill_doctors()
    fill_appointments()