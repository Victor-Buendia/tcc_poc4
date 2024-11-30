from hospital.models import *

class Paciente(Pessoa):
    tipo_sanguineo: str = Field(..., example="A+")
    peso: float = Field(..., example=80.0)

@catch
def create_patient(payload):
    did = payload["did"]

    if any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID {did} already exists")
        return "reject"
    
    AppState.patients_list[did] = payload["data"]["attributes"]
    return "accept"
    
if __name__ == "__main__":
    pac = Paciente(id=1, name="João", tipo_sanguineo="A+", peso=80)
    print(pac)
    print(pac.model_dump())