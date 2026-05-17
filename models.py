from dataclasses import dataclass, field
from abc import ABC
from datetime import datetime
import re


@dataclass
class Person(ABC):
    name: str
    age: int
    phone: str

    def __post_init__(self):
        self.validate_age()
        self.validate_phone()

    def validate_age(self):
        if not 0 < self.age < 120:
            raise ValueError("Некорректный возраст")

    def validate_phone(self):
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, self.phone):
            raise ValueError("Некорректный телефон")


@dataclass
class Patient(Person):
    _next_id = 10001

    id: int = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.id = Patient._next_id
        Patient._next_id += 1


@dataclass
class Doctor(Person):
    specialization: str
    experience: int

    _next_id = 50001
    id: int = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.id = Doctor._next_id
        Doctor._next_id += 1


@dataclass
class Appointment:
    patient: Patient
    doctor: Doctor
    date: datetime
    status: str = "scheduled"

    _next_id = 70001
    id: int = field(init=False)

    def __post_init__(self):
        self.id = Appointment._next_id
        Appointment._next_id += 1

    def complete(self):
        self.status = "completed"

    def cancel(self):
        self.status = "cancelled"


@dataclass
class RecordItem:
    doctor_name: str
    diagnosis: str
    notes: str
    date: datetime


@dataclass
class MedicalRecord:
    patient_id: int
    records: list[RecordItem] = field(default_factory=list)

    def add_record(self, doctor_name: str, diagnosis: str, notes: str):
        self.records.append(
            RecordItem(
                doctor_name=doctor_name,
                diagnosis=diagnosis,
                notes=notes,
                date=datetime.now()
            )
        )