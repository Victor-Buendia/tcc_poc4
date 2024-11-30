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
    
@frontend.get("/access_tokens", tags=["Debugging"])
def get_access_tokens():
    from hospital.api.server import inspect
    app_state = inspect("/access_tokens")
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
    from hospital.api.server import advance
    from hospital.models import Pessoa
    from hospital.api.wallet import encrypt_msg, Encryption, sym_encrypt

    import os
    import time
    import base64

    medico = Pessoa(nome="_", public_key=paciente.medico_public_key)
    key = os.urandom(32).hex()
    encrypted_data = sym_encrypt(data=paciente.shared_data, key=key)

    payload = {
        "did": paciente.did,
        "method": "create_access_token",
        "data": {
            "type": "share",
            "attributes": {
                "token": os.urandom(16).hex(),
                "patient_did": paciente.did,
                "patient_public_key": paciente.public_key,
                "doctor_did": medico.did,
                "doctor_public_key": medico.public_key,
                "shared_data": encrypted_data["encrypted_message"],
                "encrypted_iv": encrypt_msg(Encryption(message=encrypted_data["iv"], public_key=medico.public_key))["encrypted_message"],
                "encrypted_key": encrypt_msg(Encryption(message=key, public_key=medico.public_key))["encrypted_message"],
                "expires_at": time.time() + 2*60 # 2 minutes
            }
        }
    }

    result = advance(payload)
    return result