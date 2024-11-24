from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/advance")
async def advance(request: Request):
    from transaction import create_transaction

    body = await request.body()
    data = body.decode("utf-8")
    create_transaction(data)
    return {"status": "accept", "sent_data": data}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
