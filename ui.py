from exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    AppointmentError
)

class ConsoleUI:
    def __init__(self, clinic):
        self.clinic = clinic

    def show_menu(self):
        print("""
========== МЕД КЛИНИКА ==========

1. Добавить пациента
2. Добавить врача
3. Создать прием
4. Оплата
5. Список пациентов
6. Список врачей
7. Медицинская карта
8. Прайс услуг
9. История посещений
10. Статистика
11. Удалить пациента
12. Удалить врача
13. Добавить запись в медкарту
14. Список приемов
15. Отменить прием
16. Поиск врача по специализации
0. Выход
""")

    def run(self):
        while True:
            try:
                self.show_menu()

                choice = input("Выбор: ").strip()

                if choice == "1":
                    self.add_patient()

                elif choice == "2":
                    self.add_doctor()

                elif choice == "3":
                    self.create_appointment()

                elif choice == "4":
                    self.pay()

                elif choice == "5":
                    self.show_patients()

                elif choice == "6":
                    self.show_doctors()

                elif choice == "7":
                    self.show_medical_record()

                elif choice == "8":
                    self.show_price_list()

                elif choice == "9":
                    self.show_patient_history()

                elif choice == "10":
                    self.show_statistics()

                elif choice == "11":
                    self.delete_patient()

                elif choice == "12":
                    self.delete_doctor()

                elif choice == "13":
                    self.add_record()

                elif choice == "14":
                    self.show_appointments()

                elif choice == "15":
                    self.cancel_appointment()

                elif choice == "16":
                    self.find_doctors_by_specialization()

                elif choice == "0":
                    print("\nПрограмма завершена")
                    break

                else:
                    print("\nНеверный выбор")

            except (
                    PatientNotFoundError,
                    DoctorNotFoundError,
                    AppointmentError,
                    ValueError
            ) as e: print(f"\nОшибка: {e}")

    # =====================================================
    # PATIENT
    # =====================================================

    def add_patient(self):
        patient = self.clinic.add_patient(
            input("Имя: "),
            int(input("Возраст: ")),
            input("Телефон: ")
        )

        print(f"\nСоздан пациент: {patient.id}")

    def show_patients(self):
        print("\nСПИСОК ПАЦИЕНТОВ")
        print("-" * 50)

        for p in self.clinic.list_patients():
            print(f"{p.id} | {p.name} | {p.age} лет | {p.phone}")

    # =====================================================
    # DOCTOR
    # =====================================================

    def add_doctor(self):
        doctor = self.clinic.add_doctor(
            input("Имя: "),
            int(input("Возраст: ")),
            input("Телефон: "),
            input("Специализация: "),
            int(input("Опыт: "))
        )
        print(f"\nСоздан врач: {doctor.id}")

    def show_doctors(self):
        print("\nСПИСОК ВРАЧЕЙ")
        print("-" * 50)

        for d in self.clinic.list_doctors():
            print(
                f"{d.id} | "
                f"{d.name} | "
                f"{d.specialization} | "
                f"{d.experience} лет"
            )

    # =====================================================
    # APPOINTMENT
    # =====================================================

    def create_appointment(self):
        print("\nДоступные врачи:")

        for doctor in self.clinic.doctors.values():
            print(
                f"{doctor.id} | "
                f"{doctor.name} | "
                f"{doctor.specialization}"
            )

        appointment = self.clinic.create_appointment(
            input("ID пациента: "),
            input("ID врача: "),
            input("Дата (dd.mm.yyyy HH:MM): ")
        )

        print(f"\nПрием создан. ID: {appointment.id}")

    # =====================================================
    # PAYMENT
    # =====================================================

    def pay(self):
        patient_id = input("ID пациента: ")

        print("\nВрачи:")

        for doctor in self.clinic.doctors.values():

            price = self.clinic.get_service_price(
                doctor.specialization
            )

            print(
                f"{doctor.id} | "
                f"{doctor.name} | "
                f"{doctor.specialization} | "
                f"{price} руб."
            )

        doctor_id = input("\nID врача: ")

        patient, doctor, price = (
            self.clinic.pay_for_doctor(
                patient_id,
                doctor_id
            )
        )

        print("\nЧЕК")
        print("-" * 30)

        print(f"Пациент: {patient.name}")
        print(f"Врач: {doctor.name}")
        print(f"Специализация: {doctor.specialization}")
        print(f"Сумма: {price} руб.")
        print("\nОплата выполнена")

    # =====================================================
    # MEDICAL RECORD
    # =====================================================

    def show_medical_record(self):
        patient_id = input(
            "ID пациента: "
        )

        patient = self.clinic.get_patient(
            patient_id
        )

        record = (
            self.clinic.get_medical_record(
                patient_id
            )
        )

        print("\nМЕДИЦИНСКАЯ КАРТА")
        print("-" * 50)

        print(f"Пациент: {patient.name}")

        if not record.records:
            print("Записей пока нет")
            return

        for item in record.records:
            print(f"\nВрач: {item.doctor_name}")
            print(f"Диагноз: {item.diagnosis}")
            print(f"Комментарий: {item.notes}")
            print(f"Дата: {item.date.strftime('%d.%m.%Y %H:%M')}")

    # =====================================================
    # PRICE
    # =====================================================

    def show_price_list(self):

        print("\nПРАЙС УСЛУГ")
        print("-" * 50)

        prices = (self.clinic.get_price_list())

        for service, price in prices.items():
            print(f"{service}: {price} руб.")

    # =====================================================
    # HISTORY
    # =====================================================

    def show_patient_history(self):

        patient_id = input("ID пациента: ")

        appointments = (
            self.clinic.get_patient_appointments(
                patient_id
            )
        )

        print("\nИСТОРИЯ ПОСЕЩЕНИЙ")
        print("-" * 50)

        if not appointments:
            print("Посещений нет")
            return

        for app in appointments:
            print(
                f"{app.date.strftime('%d.%m.%Y %H:%M')} | "
                f"{app.doctor.name} | "
                f"{app.status}"
            )

    # =====================================================
    # STATISTICS
    # =====================================================

    def show_statistics(self):
        stats = (self.clinic.statistics())

        print("\nСТАТИСТИКА")
        print("-" * 50)
        print(f"Пациентов: {stats['patients']}")
        print(f"Врачей: {stats['doctors']}")
        print(f"Приемов: {stats['appointments']}")
        print(f"Отменено: {stats['cancelled']}")


    def delete_patient(self):

        patient_id = input("ID пациента: ")
        self.clinic.delete_patient(
            patient_id
        )

        print("\nПациент удален")

    def delete_doctor(self):

        doctor_id = input("ID врача: ")

        self.clinic.delete_doctor(
            doctor_id
        )

        print("\nВрач удален")

    def add_record(self):

        patient_id = input("ID пациента: ")
        doctor_id = input("ID врача: ")
        diagnosis = input("Диагноз: ")
        notes = input("Комментарий: ")

        self.clinic.add_record(
            patient_id,
            doctor_id,
            diagnosis,
            notes
        )

        print("\nЗапись успешно добавлена")

    def show_appointments(self):
        appointments = self.clinic.list_appointments()

        print("\nСПИСОК ПРИЕМОВ")
        print("-" * 60)

        if not appointments:
            print("Приемов пока нет")
            return

        for app in appointments:
            print(
                f"{app.id} | "
                f"{app.patient.name} | "
                f"{app.doctor.name} | "
                f"{app.date.strftime('%d.%m.%Y %H:%M')} | "
                f"{app.status}"
            )

    def cancel_appointment(self):
        appointment_id = input("ID приема: ")

        self.clinic.cancel_appointment(appointment_id)

        print("\nПрием отменен")


    def find_doctors_by_specialization(self):
        specialization = input("Специализация: ")

        doctors = self.clinic.find_doctors_by_specialization(
            specialization
        )

        print("\nНАЙДЕННЫЕ ВРАЧИ")
        print("-" * 50)

        if not doctors:
            print("Врачи не найдены")
            return

        for doctor in doctors:
            print(
                f"{doctor.id} | "
                f"{doctor.name} | "
                f"{doctor.specialization} | "
                f"{doctor.experience} лет"
            )
