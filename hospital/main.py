import json
import logging
import requests
import traceback

from os import environ
from loguru import logger
from utils import hex2str, str2hex
from hospital.state import AppState
from routes import inspect_routing, init_routing, advance_routing


rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
graphql_server = environ["GRAPHQL_SERVER_URL"]

logger.info(f"HTTP rollup_server url is {rollup_server}")

def init():
    logger.info("First run, retrieving data from Blockchain")

    response = requests.post(graphql_server, json={"query": "query notices { notices { edges { node { index input { index } payload } } } }"})
    logger.info(f"Received response ]{response.json()}")

    for notice in response.json()["data"]["notices"]["edges"]:
        payload = notice["node"]["payload"]
        data = json.loads(hex2str(payload))
        method = data["method"]
        logger.info(f"Received notice with method {method}")
        handler = init_routing[method]
        handler(data)

    logger.info("Finished Blockchain sync up, starting rollup...")


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
    logger.info(f"Received advance request data {data}")

    try:
        payload = hex2str(data["payload"])
        payload = json.loads(payload)
        logger.info(f"Received input: {payload}")

        method = payload["method"]
        logger.info(f"Received method {method}")

        handler = advance_routing[method]
        logger.info(f"Handling method {method}")

        response = handler(payload)
        color = "magenta" if response == "accept" else "red"
        logger.opt(colors=True).info(f"Method <{color}>{method}</{color}> returned status <{color}>{response}</{color}>")
        
        if response == "reject":
            return "reject"

        logger.info(f"Adding notice with payload: '{payload}'")
        add_notice(payload)

    except Exception as e:
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        add_report({"error": msg})
        return "reject"

    return "accept"


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    payload = hex2str(data["payload"])

    try:
        handler = inspect_routing[payload]
        add_report({payload: handler(payload)})
    except Exception as e:
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        add_report({"error": msg})
        return "reject"

    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}
first_run = True

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        logger.info(rollup_request)

        if first_run:
            init()
            first_run = False

        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
