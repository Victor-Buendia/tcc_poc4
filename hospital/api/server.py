from fastapi import FastAPI, Request
from wallet import encryption
from dapp import frontend
from hospital.utils import hex2str

app = FastAPI()
app.include_router(encryption)
app.include_router(frontend)


@app.get("/")
def root():
    return {"message": "Hello World"}

def advance(payload):
    import json
    from transaction import create_transaction
    create_transaction(json.dumps(payload))
    return {"status": "sent", "sent_data": payload}

def inspect(payload):
    import requests
    import json
    response = requests.get("http://localhost:8080/inspect" + payload)
    data = response.json()["reports"].pop()["payload"]
    data = hex2str(data)
    return {"status": "ok", "response": json.loads(data)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
