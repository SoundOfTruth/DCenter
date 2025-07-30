from datetime import datetime

from pydantic import (
    BaseModel, ConfigDict,
    Field, EmailStr,
    model_validator, field_serializer, model_serializer
)
from werkzeug.security import generate_password_hash


class UserSchema(BaseModel):
    email: EmailStr = Field(max_length=50)
    fullname: str = Field(min_length=8, max_length=100)


class UserCreateSchema(UserSchema):
    password: str = Field(min_length=8, max_length=50)
    repeat_password: str = Field(min_length=8, max_length=50, exclude=True)

    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='after')
    def passwords_is_similar(self):
        if self.password != self.repeat_password:
            raise ValueError("Пароли не совпадают. Повторите попытку.",)
        return self

    @field_serializer('password')
    def serialize(self, value):
        return generate_password_hash(value)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=50)
    remain: str | None = Field(default=None)

    model_config = ConfigDict(extra='forbid')


class AppointmentSchema(BaseModel):
    id: int
    patient_id: int | None
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class AppointmentsSchema(BaseModel):
    appointments: list[AppointmentSchema]

    @model_serializer
    def serialize_model(self):
        appointments_data = []
        records = []
        for idx, appointment in enumerate(self.appointments):
            appointment_date = datetime.strftime(appointment.date, "%d.%m")
            record = {
                "id": appointment.id,
                "patient_id": appointment.patient_id,
                "time": datetime.strftime(appointment.date, "%H:%M")
            }
            records.append(record)
            if (
                len(self.appointments) - 1 == idx
                or datetime.strftime(self.appointments[idx + 1].date, "%d.%m")
                != appointment_date
            ):
                appointments_data.append({
                    "date": appointment_date,
                    "records": records
                })
                records = []
        return appointments_data
