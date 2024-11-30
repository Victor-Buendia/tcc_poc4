from hospital.models import Pessoa
from hospital.api import *
from hospital.libs import *
from loguru import logger
from hospital.models import *
from hospital.state import AppState

class Paciente(Pessoa):
    tipo_sanguineo: str = Field(..., example="A+")
    peso: float = Field(..., example=80.0)


def create_patient(payload):
    did = payload["did"]

    if did in AppState.patients_list:
        logger.error(f"Patient with DID {did} already exists")
        return "reject"
    
    AppState.patients_list[did] = payload["data"]["attributes"]
    return "accept"

if __name__ == "__main__":
    pac = Paciente(id=1, name="João", tipo_sanguineo="A+", peso=80)
    print(pac)
    print(pac.model_dump())