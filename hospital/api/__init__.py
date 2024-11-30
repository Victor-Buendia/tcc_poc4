from fastapi import FastAPI, Request, APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from loguru import logger
from hospital.state import AppState
from hospital.api.transaction import create_transaction
from hospital.models.Auth import Autenticacao
from hospital.libs import *
from hospital.utils import *
from functools import wraps

def authenticate(auth: Autenticacao):
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

def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from hospital.api.server import advance

        logger.info(f"Authenticating Required for {func.__name__}")
        did = None

        for x in kwargs.values():
            if isinstance(x, Autenticacao):
                did = x.did
                logger.opt(colors=True).info(f"<black>Authenticating {x.did}...</black>")
                result = authenticate(Autenticacao(public_key=x.public_key, private_key=x.private_key))
                logger.opt(colors=True).info(f"<green>Authenticated {x.did} successfully.</green>")
            if result is None:
                logger.opt(colors=True).info(f"<red>Authentication failed for {x.did}.</red>")
                raise HTTPException(status_code=401, detail="Unauthorized.")

        logger.opt(colors=True).info(f"<cyan>Executing {func.__name__} for user {did}...</cyan>")
        result = func(*args, **kwargs)

        logger.opt(colors=True).info(f"<cyan>Executed {func.__name__} for user {did}.</cyan>")

        logger.info(f"Removing Authentication from user {did}...")
        advance({"did": did, "method": "auth_removal", "data": {}})

        return result
    return wrapper