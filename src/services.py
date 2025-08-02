import sys
from pathlib import Path

from sqlalchemy import select, and_, func, cast, Date, update
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy.exc import IntegrityError

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.models import Appointment, Clinic, Doctor, User, Speciality # noqa


class BaseService:
    def __init__(self, session: Session) -> None:
        self.session = session


class ClinicService(BaseService):

    def get(self, id: int) -> Clinic:
        return self.session.get_one(Clinic, id)

    def get_all(self) -> list[Clinic]:
        stmt = select(Clinic).order_by(Clinic.address)
        return self.session.scalars(stmt).all()  # type: ignore


class UserService(BaseService):

    def get(self, id: int) -> User | None:
        return self.session.get(User, id)

    def get_by_email(self, email: str) -> User:
        return self.session.scalar(
            select(User).filter_by(email=email)
        )  # type: ignore

    def add(self, user_schema: dict) -> User | None:
        user = User(**user_schema)
        self.session.add(user)
        try:
            self.session.flush()
            self.session.commit()
            return user
        except IntegrityError:
            self.session.rollback()
        return None


class DoctorService(BaseService):

    def get(self, id: int) -> Doctor:
        return self.session.get_one(Doctor, id)

    def get_all(self) -> list[Doctor]:
        stmt = select(Doctor).options(
            joinedload(Doctor.clinic),
            joinedload(Doctor.speciality)
        )
        return self.session.scalars(stmt).all()  # type: ignore

    def get_by_speciality(
        self, clinic_id: int, speciality_id: int
    ) -> list[Doctor]:
        stmt = select(Doctor).where(
            Doctor.clinic_id == clinic_id,
            Doctor.speciality_id == speciality_id
        )
        return self.session.scalars(stmt).all()  # type: ignore


class SpecialityService(BaseService):

    def get(self, id: int) -> Speciality:
        return self.session.get_one(Speciality, id)

    def get_all(self) -> list[Speciality]:
        stmt = select(Speciality).options(selectinload(Speciality.services))
        return self.session.scalars(stmt).all()  # type: ignore

    def get_by_clinic(self, clinic_id: int) -> list[Speciality]:
        stmt = select(Speciality).select_from(Doctor).join(
            Speciality, Speciality.id == Doctor.speciality_id
        ).where(
            Doctor.clinic_id == clinic_id
        )
        return self.session.scalars(stmt).all()  # type: ignore


class AppointmentService(BaseService):

    def get(self, id: int) -> Appointment | None:
        return self.session.get(Appointment, id)

    def get_weekly_by_doctors(self, doctor_id: int) -> list[Appointment]:
        stmt = select(
            Appointment,
        ).where(and_(
            Appointment.doctor_id == doctor_id,
            cast(Appointment.date, Date) > cast(func.now(), Date),
            cast(Appointment.date, Date) <= cast(func.now(), Date) + 7)
        ).order_by(
            Appointment.date
        )
        return self.session.scalars(stmt).all()  # type: ignore

    def take(self, id: int, user_id: int):
        stmt = select(Appointment).where(Appointment.id == id)
        appointment = self.session.scalar(stmt)
        if (
            appointment
            and not appointment.patient_id
        ):
            appointment.patient_id = user_id
            self.session.commit()
            return True
        return False

    def get_by_user(self, user_id: int) -> list[Appointment]:
        stmt = (
            select(
                Appointment).where(Appointment.patient_id == user_id).options(
                joinedload(Appointment.doctor).joinedload(Doctor.clinic)
            )
        )
        return self.session.scalars(stmt).all()  # type: ignore

    def drop(self, id: int, user_id: int) -> bool:
        stmt = update(Appointment).where(
            and_(Appointment.id == id, Appointment.patient_id == user_id)
        ).values(patient_id=None).returning(Appointment.id)
        res = self.session.execute(stmt)
        self.session.commit()
        return bool(res.scalar())
