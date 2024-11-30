from hospital.models.Paciente import Paciente, create_patient
from hospital.state import AppState
from hospital.api.transaction import create_transaction
from hospital.api import *
from hospital.libs import *
from loguru import logger

backend = APIRouter(
    prefix="/dapp",
    tags=["DApp"],
)

@backend.get("/get_appstate")
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
            "type": "Patient",
            "attributes": paciente_dict
        }
    }

    result = advance(payload)
    return result
    
