from hospital.models import *
from hospital.models.Auth import Autenticacao, verify_auth

class Medico(Pessoa):
    especialidade: str = Field(..., example="Cardiologista")
    crm: str = Field(..., example="CRM/DF 123456")

class TokenMedico(Autenticacao):
    paciente_did: str = Field(..., example="did:key:f930ed9de791aade7367240f76cf0ab22cfca2d7b957a373214abd7703fc8054")
    token: str = Field(..., example="d6c7f73a1a8f1d564314a72cd3eade62")

@catch
def create_doctor(payload):
    did = payload["did"]

    if any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID {did} already exists")
        return "reject"
    
    AppState.doctors_list[did] = payload["data"]["attributes"]
    return "accept"

@verify_auth
def access_data(payload):
    import time
    from hospital.routes import inspect_routing

    did = payload["did"]
    patient_did = payload["data"]["attributes"]["patient_did"]
    token = payload["data"]["attributes"]["token"]

    if not any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID doctor_did={did} does not exist")
        return "reject"
    elif not any(patient_did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID patient_did={patient_did} does not exist")
        return "reject"
    elif did not in AppState.doctors_list:
        logger.error(f"User with DID {did} is not a doctor")
        return "reject"
    elif AppState.access_tokens.get(patient_did) is None:
        logger.error(f"No tokens available for patient with DID {patient_did}")
        return "reject"

    expired_tokens = set()

    for token_id, token_data in AppState.access_tokens[patient_did].items():
        if all(
            [
                token_id == token,
                token_data["doctor_did"] == did,
                token_data["patient_did"] == patient_did,
                time.time() <= token_data["expires_at"],
            ]
        ):
            if AppState.allowed_reads.get(token_id) is None:
                AppState.allowed_reads[token_id] = set({did})
            else:
                AppState.allowed_reads[token_id].add(did)

            return "accept"
        else:
            if time.time() > token_data["expires_at"]:
                expired_tokens.add(token_id)
                logger.error(f"Token {token_id} for patient with DID {patient_did} expired")
            else:
                logger.error(f"Token {token} for patient with DID {patient_did} was not issued to doctor with DID {did}")

    for token_id in list(expired_tokens):
        del AppState.access_tokens[patient_did][token_id]
        if AppState.allowed_reads.get(token_id) is not None:
            AppState.allowed_reads[token_id].remove(did)

    return "reject"

if __name__ == "__main__":
    pass