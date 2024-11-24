import json
import logging
import requests
import traceback

from os import environ
from loguru import logger
from utils import hex2str, str2hex
from routes import inspect_routing, AppState


rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")


def add_notice(output):
    payload = json.dumps(output)
    response = requests.post(
        rollup_server + "/notice", json={"payload": str2hex(payload)}
    )
    logger.info(
        f"Received notice status {response.status_code} body {response.content}"
    )


def add_report(output):
    payload = json.dumps(output)
    response = requests.post(
        rollup_server + "/report", json={"payload": str2hex(payload)}
    )
    logger.info(
        f"Received report status {response.status_code} body {response.content}"
    )


def handle_advance(data):
    status = "accept"
    logger.info(f"Received advance request data {data}")

    try:
        payload = hex2str(data["payload"])
        logger.info(f"Received input: {payload}")

        output = payload
        AppState.variable += 1
        logger.debug(f"State variable is now {AppState.variable}")

        logger.info(f"Adding notice with payload: '{output}'")
        add_notice(output)

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        add_report({"error": msg})

    return status


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    payload = hex2str(data["payload"])

    response = inspect_routing[payload]
    add_report({payload: response(payload)})

    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        logger.info(rollup_request)

        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
