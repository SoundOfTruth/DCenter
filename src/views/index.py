from flask import Blueprint, render_template

from src.database.core import session_factory
from src.services import ClinicService, DoctorService, SpecialityService


router = Blueprint('index', __name__)
app = router


@app.get("/")
def index():
    with session_factory() as session:
        clinics = ClinicService(session).get_all()
    return render_template("index/index.html", clinics=clinics)


@app.get("/prices")
def prices():
    with session_factory() as session:
        specialities = SpecialityService(session).get_all()
    return render_template("index/prices.html", specialities=specialities)


@app.get("/doctors")
def doctors():
    with session_factory() as session:
        doctors = DoctorService(session).get_all()
    return render_template("index/doctors.html", doctors=doctors)
