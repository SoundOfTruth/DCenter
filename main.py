from flask import Flask, request, render_template, url_for, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:@127.0.0.1:5432/DCenter'
app.config['SECRET_KEY'] = "your secret key"
app.debug = False

db = SQLAlchemy(app=app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(user_id)
    return user


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, default=0, nullable=False)


class Clinics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speciality_id = db.Column(db.Integer, db.ForeignKey('specialities.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.id"), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(500), nullable=False)


class Specialities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    services = db.relationship('Services', backref=db.backref('specialities'))


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    speciality_id = db.Column(db.Integer, db.ForeignKey('specialities.id'), nullable=False)


@app.route('/')
def index():
    status = current_user.is_anonymous
    addresses = db.session.execute(db.select(Clinics).order_by(Clinics.name)).scalars()
    if addresses:
        return render_template("index.html", addresses=addresses, title="О нас", status=status)
    return render_template("index.html", status=status)


@app.route('/prices')
def prices():
    status = current_user.is_anonymous
    query = (
        db.select(Specialities)
    )
    specialities = db.session.execute(query).scalars().all()
    if specialities:
        return render_template('prices.html', specialities=specialities, title="Услуги и цены", status=status)
    return render_template('prices.html', status=status)


@app.route('/doctors')
def doctors():
    status = current_user.is_anonymous
    query = (db.select(Doctors))
    ds = db.session.execute(query).scalars().all()
    current_time = datetime.now()
    for doctor in ds:
        experience = str(current_time.year - int(doctor.experience))
        end_number = int(experience[len(experience)-1])
        if end_number == 1:
            experience += " год"
        elif end_number == 2 or end_number == 3 or end_number == 4:
            experience += " года"
        else:
            experience += " лет"
        doctor.experience_years = experience
        doctor_clinic = db.session.execute(db.select(Clinics.name).where(Clinics.id == doctor.clinic_id)).scalars().one()
        doctor_speciality = db.session.execute(db.select(Specialities.name).where(Specialities.id == doctor.speciality_id)).scalars().one()
        doctor.clinic = doctor_clinic
        doctor.speciality = doctor_speciality
    return render_template('doctors.html', doctors=ds, title="Специалисты", status=status)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    status = current_user.is_anonymous
    if request.method == "POST":
        user_fullname = request.form.get("username")
        user_email = request.form.get("email")
        user_password = request.form.get("password1")
        repeat_password = request.form.get("password2")
        if user_email.count("."):
            if user_password == repeat_password and len(user_password) >= 4:
                try:
                    user = Users(
                        email=user_email,
                        fullname=user_fullname,
                        password=generate_password_hash(user_password)
                    )
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('login'))
                except Exception as ex:
                    print(ex)
    return render_template('signup.html', title="Регистрация", status=status)


@app.route('/login', methods=["POST", "GET"])
def login():
    status = current_user.is_anonymous
    if request.method == "POST":
        user_email = request.form.get("email")
        input_password = request.form.get("psw")
        user = Users.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password, input_password):
                rm = True if request.form.get('remainme') else False
                if login_user(user, remember=rm):
                    return redirect(url_for('index'))
            else:
                flash("Неверный логин или пароль")
        else:
            flash("Неверный логин или пароль")
    return render_template('login.html', title="Авторизация", status=status)


@app.route('/profile')
@login_required
def profile():
    url_pattern = "/drop_appointment/"
    user = current_user
    is_empty = False
    appointment_urls = {}
    appointments = db.session.execute(db.select(Appointment).where(Appointment.patient_id == user.id)).scalars().all()
    if appointments:
        for appointment in appointments:
            doctor = db.session.execute(db.select(Doctors).where(Doctors.id == appointment.doctor_id)).scalars().one()
            address = db.session.execute(db.select(Clinics.name).where(Clinics.id == doctor.clinic_id)).scalars().one()
            appointment_urls[url_pattern+str(appointment.id)] = f"{appointment.date} {address} врач {doctor.fullname}"
    else:
        is_empty = True
    return render_template('profile.html', appointments=appointment_urls, title="Профиль",
                           status=user.is_anonymous, is_empty=is_empty, user=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/appointment/')
@login_required
def appointment_clinic():
    status = current_user.is_anonymous
    clinics = db.session.execute(db.select(Clinics).order_by(Clinics.name)).scalars()
    if clinics:
        return render_template("appointment_clinic.html", clinics=clinics, title="Запись на приём", status=status)
    return render_template("appointment_clinic.html", title="Запись на приём", status=status)


@app.route('/appointment/<int:clinic>')
@login_required
def appointment_speciality(clinic):
    status = current_user.is_anonymous
    specialities = db.session.execute(db.select(Specialities).order_by(Specialities.name)).scalars()
    if specialities:
        clinic_address = db.session.execute(db.select(Clinics.name).where(Clinics.id == clinic)).scalars().one()
        return render_template("appointment_speciality.html", specialities=specialities, path=clinic,
                               title=f"Запись на приём {clinic_address}", status=status)
    return render_template("appointment_speciality.html", status=status)


@app.route('/appointment/<int:clinic>/<int:speciality>')
@login_required
def appointment_doctor(clinic, speciality):
    status = current_user.is_anonymous
    str_path = str(clinic) + "/" + str(speciality)
    data = db.session.execute(db.select(Doctors).where(Doctors.speciality_id == speciality)
                                      .where(Doctors.clinic_id == clinic)).scalars().all()
    if data:
        speciality_name = db.session.execute(db.select(Specialities.name).where(Specialities.id == speciality)).scalars().one()
        clinic_address = db.session.execute(db.select(Clinics.name).where(Clinics.id == clinic)).scalars().one()
        return render_template("appointment_doctor.html", doctors=data, path=str_path,
                               title=f"Запись на приём {clinic_address}. {speciality_name}.", status=status)
    return render_template("appointment_doctor.html", status=status)


@app.route('/appointment/<int:clinic>/<int:speciality>/<int:doctor>')
@login_required
def choose_appointment(clinic, speciality, doctor):
    status = current_user.is_anonymous
    appointments = db.session.execute(db.select(Appointment)
                                      .where(Appointment.doctor_id == doctor)
                                      .order_by(Appointment.date)
                                      ).scalars().all()
    dict_app = {}
    for appointment in appointments:
        url_pattern = "/take_appointment/"
        date = appointment.date
        time_urls = {}
        for times in appointments:
            if datetime.strftime(date, '%d.%m') == datetime.strftime(times.date, '%d.%m'):
                url = url_pattern+str(times.id)
                if times.patient_id != 0:
                    url = f"0+{str(times.id)}"
                time_urls[url] = datetime.strftime(times.date, '%H:%M')
        dict_app[datetime.strftime(date, '%d.%m')] = time_urls
    doctor_name = db.session.execute(db.select(Doctors.fullname).where(Doctors.id == doctor)).scalars().one()
    if appointments:
        speciality_name = db.session.execute(db.select(Specialities.name).where(Specialities.id == speciality)).scalars().one()
        clinic_address = db.session.execute(db.select(Clinics.name).where(Clinics.id == clinic)).scalars().one()
        return render_template("appointments.html", appointments=dict_app,
                               title=f"Запись на приём {clinic_address}. {speciality_name}. {doctor_name}.",
                               status=status)
    return render_template("appointments.html", status=status)


@app.route('/take_appointment/<int:id>')
@login_required
def take_appointment(id):
    user = current_user
    query = (db.select(Appointment).where(Appointment.id == id))
    cur_appointment = db.session.execute(query).scalars().one()
    if cur_appointment and cur_appointment.patient_id == 0:
        update = db.update(Appointment).where(Appointment.id == id).values(patient_id=user.id)
        db.session.execute(update)
        db.session.commit()
    return redirect(url_for('profile'))


@app.route('/drop_appointment/<int:id>')
@login_required
def drop_appointment(id):
    user = current_user
    query = (db.select(Appointment).where(Appointment.id == id))
    cur_appointment = db.session.execute(query).scalars().one()
    if cur_appointment and cur_appointment.patient_id == user.id:
        update = db.update(Appointment).where(Appointment.id == id).values(patient_id=0)
        db.session.execute(update)
        db.session.commit()
    return redirect(url_for('profile'))


@app.errorhandler(404)
def page_not_found(error):
    status = current_user.is_anonymous
    return render_template('page404.html', status=status), 404


if __name__ == '__main__':
    app.run()
