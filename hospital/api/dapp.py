from hospital.models.Paciente import Paciente, TokenPaciente, create_patient
from hospital.models.Medico import Medico, create_doctor
from hospital.api import *

frontend = APIRouter(
    prefix="/dapp",
    tags=["DApp"],
)

@frontend.post("/authenticate", tags=["Debugging"])
def authenticate_transaction(auth: Autenticacao):
    return authenticate(auth)

@frontend.get("/appstate", tags=["Debugging"])
def get_appstate():
    from hospital.api.server import inspect
    app_state = inspect("/appstate")
    return app_state

@frontend.get("/pending_auths", tags=["Debugging"])
def get_pending_auths():
    from hospital.api.server import inspect
    app_state = inspect("/pending_auths")
    return app_state

@frontend.get("/valid_auths", tags=["Debugging"])
def get_valid_auths():
    from hospital.api.server import inspect
    app_state = inspect("/valid_auths")
    return app_state

@frontend.post("/create_patient", tags=["Frontend"])
def create_patient_transaction(paciente: Paciente):
    from hospital.api.server import advance

    payload = {
        "did": paciente.did,
        "method": "create_patient",
        "data": {
            "type": "patient",
            "attributes": paciente.model_dump()
        }
    }

    result = advance(payload)
    return result

@frontend.post("/create_doctor", tags=["Frontend"])
def create_doctor_transaction(medico: Medico):
    from hospital.api.server import advance

    payload = {
        "did": medico.did,
        "method": "create_doctor",
        "data": {
            "type": "doctor",
            "attributes": medico.model_dump()
        }
    }

    result = advance(payload)
    return result

@frontend.post("/create_access_token", tags=["Frontend"])
@auth
def create_access_token_transaction(paciente: TokenPaciente):
    import time
    time.sleep(5)
    pass