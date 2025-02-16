from pydantic import BaseModel, Field
from hospital.libs import *
from loguru import logger
from hospital.state import AppState
from functools import wraps

import time

def verify_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        did = args[0]["did"]

        if did not in AppState.valid_auths:
            logger.error(f"DID {did} is not authenticated")
            return "reject"
        elif time.time() > AppState.valid_auths[did]["expires_at"]:
            logger.error(f"Authentication for DID {did} has expired")
            return "reject"

        return func(*args, **kwargs)
    return wrapper

def catch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {e}")
            return "reject"
    return wrapper

class Pessoa(BaseModel):
    nome: str = Field(..., example="João")
    public_key: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")

    @property
    def did(self):
        return "did:key:" + hash_text_sha256(self.public_key)

