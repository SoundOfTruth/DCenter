from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_required  # type: ignore

from src.database.core import session_factory
from src.services import (
    AppointmentService,
    ClinicService,
    DoctorService,
    SpecialityService
)
from src.schemas import AppointmentSchema, AppointmentsSchema
from src.models import User


router = Blueprint(
    name='appointment',
    import_name=__name__,
    url_prefix='/appointment'
)

app = router
current_user: User = current_user


@app.get("/")
def index():
    with session_factory() as session:
        clinics = ClinicService(session).get_all()
    return render_template(
        "appointment/index.html", clinics=clinics
    )


@app.get("/clinic/<int:clinic_id>")
def clinic_specialities(clinic_id):
    with session_factory() as session:
        specialities = SpecialityService(session).get_by_clinic(clinic_id)
    return render_template(
        "appointment/speciality.html", specialities=specialities
    )


@app.get("/clinic/<int:clinic_id>/speciality/<int:speciality_id>")
def doctors(clinic_id, speciality_id):
    with session_factory() as session:
        doctors = DoctorService(session).get_by_speciality(
            clinic_id, speciality_id
        )
    return render_template(
        "appointment/doctor.html", doctors=doctors
    )


@app.get("/doctor/<doctor_id>")
def appointments(doctor_id):
    with session_factory() as session:
        appointments = AppointmentService(
            session).get_weekly_by_doctors(doctor_id)
    appointment_schemas = [
        AppointmentSchema.model_validate(appointment)
        for appointment in appointments
    ]
    appointments_schema = AppointmentsSchema(appointments=appointment_schemas)
    return render_template(
        "appointment/appointments.html",
        appointments=appointments_schema.model_dump()
    )


@app.post("/take/<int:id>")
@login_required
def take(id: int):
    with session_factory() as session:
        is_taken = AppointmentService(session).take(id, current_user.id)
    message, status = "Вы успешно записались на приём", "success"
    if not is_taken:
        message, status = "Ошибка", "error"
    flash(message, status)
    return redirect(url_for("auth.profile"))


@app.post("/drop/<int:id>")
@login_required
def drop(id: int):
    if request.method == "POST":
        with session_factory() as session:
            appointment = AppointmentService(session).get(id)
            if appointment and appointment.patient_id == current_user.id:
                appointment.patient_id = None
                session.commit()
                flash("Запись успешно отменена", "success")
    return redirect(url_for("auth.profile"))
