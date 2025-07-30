import datetime
from typing import Annotated

from sqlalchemy import String, ForeignKey, func, cast, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from flask_login import UserMixin

from src.database.core import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Clinic(Base):
    __tablename__ = "clinics"

    id: Mapped[int_pk]
    address: Mapped[str] = mapped_column(String(50), unique=True)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="clinic")


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int_pk]
    fullname: Mapped[str] = mapped_column(String(50))
    qualification: Mapped[str] = mapped_column(String(100))
    photo: Mapped[str | None] = mapped_column(String(255), default=None)
    experience_start: Mapped[int] = mapped_column()
    experience = column_property(
        cast(func.extract("year", func.now()) - experience_start, Integer)
    )

    speciality_id: Mapped[int] = mapped_column(
        ForeignKey("specialities.id", ondelete="CASCADE")
    )
    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id", ondelete="CASCADE")
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor"
    )
    clinic: Mapped["Clinic"] = relationship(back_populates="doctors")
    speciality: Mapped["Speciality"] = relationship(back_populates="doctors")


class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(50), unique=True)
    fullname: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(500))

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient"
    )


class Speciality(Base):
    __tablename__ = 'specialities'

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50), unique=True)

    services: Mapped[list["Service"]] = relationship(
        back_populates="speciality"
    )
    doctors: Mapped[list["Doctor"]] = relationship(
        back_populates="speciality"
    )


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[str] = mapped_column(String(50))
    speciality_id = mapped_column(
        ForeignKey("specialities.id", ondelete="CASCADE")
    )

    speciality: Mapped["Speciality"] = relationship(back_populates="services")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int_pk]
    date: Mapped[datetime.datetime]

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE")
    )
    patient_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), default=None
    )

    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    patient: Mapped["User"] = relationship(back_populates="appointments")
