class ClinicError(Exception):
    pass


class PatientNotFoundError(ClinicError):
    pass


class DoctorNotFoundError(ClinicError):
    pass


class AppointmentError(ClinicError):
    pass