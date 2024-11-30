from hospital.models.Paciente import create_patient
from hospital.models.Medico import create_doctor
from hospital.state import AppState

inspect_routing = {
    "app_state": lambda _: {"AppState": {k:v for k,v in vars(AppState).items() if not k.startswith("__")}},
    "patient_list": lambda _: AppState.patients_list
}

init_routing = {
    "create_patient": create_patient,
    "create_doctor": create_doctor
}

advance_routing = {
    "create_patient": create_patient,
    "create_doctor": create_doctor,
}