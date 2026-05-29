from services import ClinicService
from ui import ConsoleUI


def fill_test_data(clinic):
    clinic.add_patient("Сидор Сидоров", 34, "+79991234567", log=False)
    clinic.add_patient("Лариса Долина", 28, "+79997654321", log=False)
    clinic.add_patient("Райан Гослинг", 45, "+79990001122", log=False)
    clinic.add_patient("Ильина Арина", 19, "+79990001422", log=False)
    clinic.add_patient("Игорь Синяк", 30, "+79980001122", log=False)

    clinic.add_doctor("Доктор Айболитов", 40, "+79991112233", "Терапевт", 15, log=False)
    clinic.add_doctor("Доктор Пеппер", 38, "+79994445566", "Кардиолог", 12, log=False)
    clinic.add_doctor("Доктор Плюшева", 35, "+79997778899", "Невролог", 9, log=False)


def main():
    clinic = ClinicService("ClinicManager")

    clinic.load_data()

    if not clinic.patients:
        fill_test_data(clinic)

    ui = ConsoleUI(clinic)

    try:
        ui.run()
    finally:
        clinic.save_data()


if __name__ == "__main__":
    main()
