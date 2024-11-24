def hex2str(hex):
    return bytes.fromhex(hex[2:]).decode("utf-8")


def str2hex(str):
    return "0x" + str.encode("utf-8").hex()
