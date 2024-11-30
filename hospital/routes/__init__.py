from hospital.models.Paciente import create_patient
from hospital.models.Medico import create_doctor
from hospital.models.Auth import *
from hospital.state import AppState

def _pass(payload):
    pass

inspect_routing = {
    "appstate": lambda _: {"AppState": {k:v for k,v in vars(AppState).items() if not k.startswith("__")}},
    "patient_list": lambda _: AppState.patients_list,
    "doctor_list": lambda _: AppState.doctors_list,
    "pending_auths": lambda _: AppState.pending_auths,
    "valid_auths": lambda _: AppState.valid_auths,
}

advance_routing = {
    "create_patient": create_patient,
    "create_doctor": create_doctor,
    "auth_request": authenticate_request,
    "auth_response": authenticate_response,
    "auth_attempt": attempt_authentication,
}

init_routing = advance_routing.copy()
init_routing["auth_request"] = _pass
init_routing["auth_response"] = _pass
init_routing["auth_attempt"] = _pass