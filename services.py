import logging
from datetime import datetime

from storage import Storage

from models import (
    Patient,
    Doctor,
    Appointment,
    MedicalRecord
)

from exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    AppointmentError
)


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


class ClinicService:

    def __init__(self, name: str):
        self.name = name

        self.patients: dict[int, Patient] = {}
        self.doctors: dict[int, Doctor] = {}
        self.appointments: dict[int, Appointment] = {}
        self.records: dict[int, MedicalRecord] = {}

    # =====================================================
    # PATIENTS
    # =====================================================

    def add_patient(self, name: str, age: int, phone: str, log: bool = True) -> Patient:
        patient = Patient(name, age, phone)

        self.patients[patient.id] = patient
        self.records[patient.id] = MedicalRecord(patient.id)

        if log:
            logging.info(f"Пациент добавлен: {patient.name}")

        return patient

    def get_patient(self, patient_id) -> Patient:
        try:
            patient_id = int(patient_id)
        except ValueError:
            raise PatientNotFoundError("ID пациента должен быть числом")

        patient = self.patients.get(patient_id)

        if not patient:
            raise PatientNotFoundError("Пациент не найден")

        return patient

    def delete_patient(self, patient_id):
        patient = self.get_patient(patient_id)

        appointments_to_delete = []

        for appointment in self.appointments.values():
            if appointment.patient.id == patient.id:
                appointments_to_delete.append(appointment.id)

        for appointment_id in appointments_to_delete:
            del self.appointments[appointment_id]

        if patient.id in self.records:
            del self.records[patient.id]

        del self.patients[patient.id]

        logging.info(f"Пациент удален: {patient.name}")

    def list_patients(self):
        return list(self.patients.values())

    # =====================================================
    # DOCTORS
    # =====================================================

    def add_doctor(
            self,
            name: str,
            age: int,
            phone: str,
            specialization: str,
            experience: int,
            log: bool = True
    ) -> Doctor:
        doctor = Doctor(
            name=name,
            age=age,
            phone=phone,
            specialization=specialization,
            experience=experience
        )

        self.doctors[doctor.id] = doctor

        if log:
            logging.info(f"Врач добавлен: {doctor.name}")

        return doctor

    def get_doctor(self, doctor_id) -> Doctor:
        try:
            doctor_id = int(doctor_id)
        except ValueError:
            raise DoctorNotFoundError("ID врача должен быть числом")

        doctor = self.doctors.get(doctor_id)

        if not doctor:
            raise DoctorNotFoundError("Врач не найден")

        return doctor

    def delete_doctor(self, doctor_id):
        doctor = self.get_doctor(doctor_id)

        appointments_to_delete = []

        for appointment in self.appointments.values():
            if appointment.doctor.id == doctor.id:
                appointments_to_delete.append(
                    appointment.id
                )

        for appointment_id in appointments_to_delete:
            del self.appointments[appointment_id]

        del self.doctors[doctor.id]

        logging.info(
            f"Врач удален: {doctor.name}"
        )

    def list_doctors(self):
        return list(self.doctors.values())

    def find_doctors_by_specialization(self, specialization: str):
        return [
            doctor for doctor in self.doctors.values()
            if doctor.specialization.lower() == specialization.lower()
        ]

    # =====================================================
    # APPOINTMENTS
    # =====================================================

    def create_appointment(self, patient_id, doctor_id, date_str: str) -> Appointment:
        patient = self.get_patient(patient_id)
        doctor = self.get_doctor(doctor_id)

        date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        if date < datetime.now():
            raise AppointmentError(
                "Нельзя создать прием в прошлом"
            )

        for app in self.appointments.values():
            if app.doctor.id == doctor.id and app.date == date and app.status == "scheduled":
                raise AppointmentError("Врач уже занят на это время")

        appointment = Appointment(patient, doctor, date)
        self.appointments[appointment.id] = appointment

        logging.info(f"Создан прием: {appointment.id}")

        return appointment

    def get_appointment(self, appointment_id) -> Appointment:
        try:
            appointment_id = int(appointment_id)
        except ValueError:
            raise AppointmentError("ID приема должен быть числом")

        appointment = self.appointments.get(appointment_id)

        if not appointment:
            raise AppointmentError("Прием не найден")

        return appointment

    def list_appointments(self):
        return list(self.appointments.values())

    def cancel_appointment(self, appointment_id):
        appointment = self.get_appointment(appointment_id)

        if appointment.status != "scheduled":
            raise AppointmentError("Можно отменить только запланированный прием")

        appointment.cancel()

        logging.info(f"Прием отменен: {appointment.id}")


    def get_patient_appointments(self, patient_id):
        patient = self.get_patient(patient_id)

        return [
            appointment for appointment in self.appointments.values()
            if appointment.patient.id == patient.id
        ]

    # =====================================================
    # MEDICAL RECORDS
    # =====================================================

    def get_medical_record(self, patient_id) -> MedicalRecord:
        patient = self.get_patient(patient_id)

        record = self.records.get(patient.id)

        if not record:
            record = MedicalRecord(patient.id)
            self.records[patient.id] = record

        return record

    # =====================================================
    # PRICE AND PAYMENT
    # =====================================================

    def get_price_list(self):
        return {
            "Терапевт": 1500,
            "Кардиолог": 2500,
            "Невролог": 2200,
            "Хирург": 3000,
            "Стоматолог": 2800,
        }

    def get_service_price(self, specialization: str) -> float:
        price_list = self.get_price_list()
        return price_list.get(specialization, 2000)

    def pay_for_doctor(self, patient_id, doctor_id):
        patient = self.get_patient(patient_id)
        doctor = self.get_doctor(doctor_id)

        price = self.get_service_price(doctor.specialization)

        return patient, doctor, price

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):
        return {
            "patients": len(self.patients),
            "doctors": len(self.doctors),
            "appointments": len(self.appointments),
            "completed": len([
                app for app in self.appointments.values()
                if app.status == "completed"
            ]),
            "cancelled": len([
                app for app in self.appointments.values()
                if app.status == "cancelled"
            ])
        }

    # =====================================================
    # SAVE / LOAD
    # =====================================================

    def save_data(self):
        data = {
            "patients": [],
            "doctors": [],
            "appointments": [],
            "records": []
        }

        for p in self.patients.values():
            data["patients"].append({
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "phone": p.phone
            })

        for d in self.doctors.values():
            data["doctors"].append({
                "id": d.id,
                "name": d.name,
                "age": d.age,
                "phone": d.phone,
                "specialization": d.specialization,
                "experience": d.experience
            })

        for a in self.appointments.values():
            data["appointments"].append({
                "id": a.id,
                "patient_id": a.patient.id,
                "doctor_id": a.doctor.id,
                "date": a.date.strftime("%d.%m.%Y %H:%M"),
                "status": a.status
            })
        for patient_id, record in self.records.items():
            for item in record.records:
                data["records"].append({
                    "patient_id": patient_id,
                    "doctor_name": item.doctor_name,
                    "diagnosis": item.diagnosis,
                    "notes": item.notes,
                    "date": item.date.strftime("%d.%m.%Y %H:%M")
                })
        Storage.save(data)

    def load_data(self):
        data = Storage.load()

        for item in data.get("patients", []):
            patient = Patient(
                name=item["name"],
                age=item["age"],
                phone=item["phone"]
            )

            patient.id = item["id"]

            self.patients[patient.id] = patient
            self.records[patient.id] = MedicalRecord(patient.id)

        for item in data.get("doctors", []):
            doctor = Doctor(
                name=item["name"],
                age=item["age"],
                phone=item["phone"],
                specialization=item["specialization"],
                experience=item["experience"]
            )

            doctor.id = item["id"]

            self.doctors[doctor.id] = doctor

        for item in data.get("appointments", []):
            patient = self.patients.get(item["patient_id"])
            doctor = self.doctors.get(item["doctor_id"])

            if patient and doctor:
                date = datetime.strptime(item["date"], "%d.%m.%Y %H:%M")

                appointment = Appointment(patient, doctor, date)
                appointment.id = item["id"]
                appointment.status = item["status"]

                self.appointments[appointment.id] = appointment

        for item in data.get("records", []):
            patient_id = int(item["patient_id"])

            if patient_id not in self.records:
                self.records[patient_id] = MedicalRecord(patient_id)

            self.records[patient_id].add_record(
                item["doctor_name"],
                item["diagnosis"],
                item["notes"]
            )

            self.records[patient_id].records[-1].date = datetime.strptime(
                item["date"],
                "%d.%m.%Y %H:%M"
            )

        if self.patients:
            Patient._next_id = max(self.patients.keys()) + 1

        if self.doctors:
            Doctor._next_id = max(self.doctors.keys()) + 1

        if self.appointments:
            Appointment._next_id = max(self.appointments.keys()) + 1


    def add_record(
            self,
            patient_id,
            doctor_id,
            diagnosis,
            notes
    ):
        patient = self.get_patient(patient_id)
        doctor = self.get_doctor(doctor_id)

        record = self.get_medical_record(
            patient.id
        )

        record.add_record(
            doctor.name,
            diagnosis,
            notes
        )

        logging.info(
            "Запись добавлена"
        )