import hmac
import hashlib
import struct
import time
import base64
import requests

def totp_sha512(secret: bytes, time_step: int = 30, t0: int = 0, digits: int = 10, for_time: int | None = None) -> str:
    """
    RFC 6238 TOTP with HMAC-SHA-512 and dynamic truncation.
    - secret: raw bytes (ASCII of email + "HENNGECHALLENGE004")
    - digits: number of decimal digits in the output (10 here)
    """
    if for_time is None:
        for_time = int(time.time())

    # Moving factor T = floor((currentTime - T0) / X)
    counter = (for_time - t0) // time_step

    # 8-byte big-endian counter
    msg = struct.pack(">Q", counter)

    hmac_hash = hmac.new(secret, msg, hashlib.sha512).digest()

    # Dynamic truncation (per RFC 4226)
    offset = hmac_hash[-1] & 0x0F
    four_bytes = hmac_hash[offset:offset + 4]
    code_int = struct.unpack(">I", four_bytes)[0] & 0x7FFFFFFF  # 31-bit

    code_mod = code_int % (10 ** digits)
    return str(code_mod).zfill(digits)

def make_auth_header(email: str, password: str) -> str:
    token = f"{email}:{password}".encode("ascii")
    b64 = base64.b64encode(token).decode("ascii")
    return f"Basic {b64}"

if __name__ == "__main__":
    email = "hilal560anwar@gmail.com"
    secret = (email + "HENNGECHALLENGE004").encode("ascii")

    otp = totp_sha512(secret, time_step=30, t0=0, digits=10)
    print("Current 10-digit TOTP:", otp)

    url = "https://api.challenge.hennge.com/challenges/backend-recursion/004"
    payload = {
        "github_url": "https://gist.github.com/24F3004969/097467fe0512cd0bd8dbc747827a1341",
        "contact_email": email,
        "solution_language": "python"
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Authorization": make_auth_header(email, otp)
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    print(resp.status_code)
    print(resp.text)