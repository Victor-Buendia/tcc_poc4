from hospital.models.Paciente import create_patient, share_data, remove_token
from hospital.models.Medico import create_doctor, access_data
from hospital.models.Auth import authenticate_request, authenticate_response, attempt_authentication, remove_auth
from hospital.state import AppState

def _pass(payload):
    pass

inspect_routing = {
    "appstate": lambda _: {"AppState": {k:v for k,v in vars(AppState).items() if not k.startswith("__")}},
    "patient_list": lambda _: AppState.patients_list,
    "doctor_list": lambda _: AppState.doctors_list,
    "pending_auths": lambda _: AppState.pending_auths,
    "valid_auths": lambda _: AppState.valid_auths,
    "access_tokens": lambda _: AppState.access_tokens,
    "allowed_reads": lambda _: AppState.allowed_reads,
}

advance_routing = {
    "create_patient": create_patient,
    "create_doctor": create_doctor,
    "auth_request": authenticate_request,
    "auth_response": authenticate_response,
    "auth_attempt": attempt_authentication,
    "auth_removal": remove_auth,
    "create_access_token": share_data,
    "access_data": access_data,
    "remove_token": remove_token,
}

init_routing = advance_routing.copy()
init_routing["auth_request"] = _pass
init_routing["auth_response"] = _pass
init_routing["auth_attempt"] = _pass