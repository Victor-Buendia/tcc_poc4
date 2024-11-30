from hospital.models.Paciente import Paciente, create_patient
from hospital.models.Medico import Medico, create_doctor
from hospital.api import *

backend = APIRouter(
    prefix="/dapp",
    tags=["DApp"],
)

@backend.get("/appstate")
def get_appstate():
    from hospital.api.server import inspect
    app_state = inspect("/app_state")
    return app_state

@backend.post("/create_patient")
def create_patient_transaction(paciente: Paciente):
    from hospital.api.server import advance

    paciente_dict = paciente.model_dump()
    did = "did:key:" + hash_text_sha256(paciente_dict['public_key'])

    payload = {
        "did": did,
        "method": "create_patient",
        "data": {
            "type": "patient",
            "attributes": paciente_dict
        }
    }

    result = advance(payload)
    return result

@backend.post("/create_doctor")
def create_doctor_transaction(medico: Medico):
    from hospital.api.server import advance

    medico_dict = medico.model_dump()
    did = "did:key:" + hash_text_sha256(medico_dict['public_key'])

    payload = {
        "did": did,
        "method": "create_doctor",
        "data": {
            "type": "doctor",
            "attributes": medico_dict
        }
    }

    result = advance(payload)
    return result
    
