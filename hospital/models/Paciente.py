from hospital.models import *
from hospital.models.Auth import Autenticacao

class Paciente(Pessoa):
    tipo_sanguineo: str = Field(..., example="A+")
    peso: float = Field(..., example=80.0)

class TokenPaciente(Autenticacao):
    medico_public_key: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541726e335545615a3848786a6358466c4e455939700a536139702f366251757074414c57764d64635330557034394179777662565a4752337841744369545759744f43526c3650757346437357484e6a4762537157410a344c39697a6d76796863525a36664f4b354b7375492b427a6a704f556a416b713475556d464a6d314a336347334c3645546153573237302f7a49634842484d380a3269586b3945304856354c506e66536e6134585150315477673476684c726136372f436a6e424846314643464d52556c5a517447375533784a6f6e46736c6e740a44527a565245686f786c79767032534e6b743352506577786677593446444e6c5a7a336a616e656235636761592b74394b6f37464a4e4f555a38567530666a6a0a366a37724374436b30695170742b724f497456357a70745350384844315a71335852675a4b343870325a633949716871475449666b374e574743564d315777560a4d514944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")
    shared_data: str = Field(..., example='{"laudo": "Paciente com febre", "doenca": "Gripe"}')

def remove_token(payload):
    did = payload["did"]
    patient_did = payload["data"]["attributes"]["patient_did"]
    doctor_did = payload["data"]["attributes"]["doctor_did"]
    token = payload["data"]["attributes"]["token"]
    
    if AppState.access_tokens.get(patient_did).get(token):
        del AppState.access_tokens[patient_did][token]
    if AppState.allowed_reads.get(doctor_did) == token:
        del AppState.allowed_reads[doctor_did]

    return "accept"

@catch
def create_patient(payload):
    did = payload["did"]

    if any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID {did} already exists")
        return "reject"
    
    AppState.patients_list[did] = payload["data"]["attributes"]
    return "accept"

# @verify_auth
def share_data(payload):
    import time
    import json
    import os

    did = payload["did"]
    if did not in AppState.patients_list:
        logger.error(f"User with DID {did} does not exist")
        return "reject"
        
    token = payload["data"]["attributes"]["token"]
    shared_data = payload["data"]["attributes"]["shared_data"]

    if AppState.access_tokens.get(did) is None:
        AppState.access_tokens[did] = {}

    acc_token_data = {
        "patient_did": payload["data"]["attributes"]["patient_did"],
        "doctor_did": payload["data"]["attributes"]["doctor_did"],
        "shared_data": shared_data,
        "encrypted_key": payload["data"]["attributes"]["encrypted_key"],
        "encrypted_iv": payload["data"]["attributes"]["encrypted_iv"],
        "expires_at": payload["data"]["attributes"]["expires_at"],
    }

    AppState.access_tokens[did][token] = acc_token_data

    return "accept"
    
if __name__ == "__main__":
    pac = Paciente(id=1, name="João", tipo_sanguineo="A+", peso=80)
    print(pac)
    print(pac.model_dump())