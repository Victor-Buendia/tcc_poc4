from hospital.models.Paciente import Paciente, create_patient
from hospital.models.Medico import Medico, create_doctor
from hospital.models.Auth import Autenticacao
from hospital.api import *

frontend = APIRouter(
    prefix="/dapp",
    tags=["DApp"],
)

@frontend.get("/appstate")
def get_appstate():
    from hospital.api.server import inspect
    app_state = inspect("/appstate")
    return app_state

@frontend.get("/pending_auths")
def get_pending_auths():
    from hospital.api.server import inspect
    app_state = inspect("/pending_auths")
    return app_state

@frontend.get("/valid_auths")
def get_valid_auths():
    from hospital.api.server import inspect
    app_state = inspect("/valid_auths")
    return app_state

@frontend.post("/create_patient")
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

@frontend.post("/create_doctor")
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
    
@frontend.post("/authenticate")
def authenticate_transaction(auth: Autenticacao):
    from hospital.api.wallet import sign_msg, Decryption
    from hospital.api.server import advance, inspect
    import os

    payload = {
        "did": auth.did,
        "method": "auth_request",
        "data": {
            "public_key": auth.public_key
        },
    }
    result = advance(payload)

    @listen()
    def get_pending_auth():
        pending_auths = inspect("/pending_auths")
        return pending_auths["response"]["pending_auths"].get(auth.did)

    attempt = get_pending_auth()
    if not attempt:
        raise HTTPException(status_code=404, detail="No pending authentication attempt. User probably doesn't exist or there was a problem with the authentication request.")

    proof = sign_msg(Decryption(message=attempt["challenge"], private_key=auth.private_key))
    payload = {
        "did": auth.did,
        "method": "auth_response",
        "data": {
            "proof": proof["signature"],
        },
    }
    result = advance(payload)

    attempt = get_pending_auth()
    payload = {
        "did": auth.did,
        "method": "auth_attempt",
        "data": {}
    }
    result = advance(payload)

    @listen()
    def get_auth():
        valid_auths = inspect("/valid_auths")
        return valid_auths["response"]["valid_auths"].get(auth.did)

    final_auth = get_auth()
    if not final_auth:
        raise HTTPException(status_code=404, detail="Authentication rejected.")

    return final_auth
