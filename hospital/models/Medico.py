from hospital.models import *

class Medico(Pessoa):
    especialidade: str = Field(..., example="Cardiologista")
    crm: str = Field(..., example="123456")

@catch
def create_doctor(payload):
    did = payload["did"]

    if any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID {did} already exists")
        return "reject"
    
    AppState.doctors_list[did] = payload["data"]["attributes"]
    return "accept"

if __name__ == "__main__":
    pass