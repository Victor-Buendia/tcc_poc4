from loguru import logger

import json
import pexpect
import tempfile


def create_transaction(input_data: str, account_id: int = 1) -> None:
    command = [
        "cartesi",
        "send",
        "generic",
        "--rpc-url",
        "http://localhost:8545",
        f"--input='{input_data}'",
    ]
    logger.info(f"Command: {' '.join(command)}")
    account = "".join(
        [chr(27) + "[B"] * (account_id - 1)
    )  # \x1b[B is the escape sequence for the down arrow key

    with tempfile.NamedTemporaryFile(delete=False, mode="w+") as temp_log_file:
        log_file_path = temp_log_file.name

    child = pexpect.spawn(" ".join(command), logfile=open(log_file_path, "wb"))

    try:
        child.expect([r"Chain"])
        child.sendline("")

        child.expect([r"Wallet"])
        child.sendline("")

        child.expect(r"Mnemonic.*")
        mnemonic = "test test test test test test test test test test test junk"
        child.sendline(mnemonic)

        child.expect(r"Account.*")
        child.send(account)
        child.sendline("")

        child.expect([r"address"])
        child.sendline("")

        child.expect(r"Input sent.*")
        child.wait()

    finally:
        child.close()
        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()
            logger.info(f"Process output: \n{log_content}")


if __name__ == "__main__":
    data = {
        "name": "Victor",
        "age": 25,
    }
    logger.info(f"Creating transaction with data: {data}")
    create_transaction(json.dumps(data))
