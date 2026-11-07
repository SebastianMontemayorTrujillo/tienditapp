"""Cliente mínimo de la API de pey y verificación de webhooks (Standard Webhooks)."""
import base64
import hashlib
import hmac
import json
import socket
import time
import urllib.error
import urllib.request

BASE_URL = "https://api.pey.mx"


class PeyError(Exception):
    def __init__(self, type_: str, message: str = ""):
        super().__init__(f"{type_}: {message}")
        self.type = type_


class PeyTimeout(Exception):
    """La solicitud no tuvo respuesta: el cobro queda incierto y se debe conciliar."""


class PeyClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 15.0):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    def _call(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read()).get("error", {})
            except Exception:
                err = {}
            raise PeyError(err.get("type", f"HTTP_{e.code}"), err.get("message", ""))
        except (socket.timeout, TimeoutError, urllib.error.URLError) as e:
            raise PeyTimeout(str(e))

    def create_qr(self, amount_pesos: float, concept: str, expiration_sec: int, sale_id: str) -> dict:
        return self._call("POST", "/codi/qr", {
            "amount": amount_pesos,
            "concept": concept[:40],
            "expiration": expiration_sec,
            "generateImage": True,
            "metadata": {"saleId": sale_id},
        })

    def qr_transactions(self, qr_id: str) -> list[dict]:
        return self._call("GET", f"/transaction/codi/qr/{qr_id}").get("items", [])


def verify_webhook(headers: dict, raw_body: bytes, secret: str, tolerance_sec: int = 300) -> bool:
    """Standard Webhooks: firma HMAC-SHA256 de "{id}.{timestamp}.{body}" con el secreto whsec_."""
    msg_id = headers.get("webhook-id", "")
    ts = headers.get("webhook-timestamp", "")
    signatures = headers.get("webhook-signature", "")
    if not (msg_id and ts and signatures and secret):
        return False
    try:
        if abs(time.time() - int(ts)) > tolerance_sec:
            return False
        key = base64.b64decode(secret.split("_", 1)[1] if secret.startswith("whsec_") else secret)
    except (ValueError, IndexError):
        return False
    signed = f"{msg_id}.{ts}.".encode() + raw_body
    expected = base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()
    candidates = [s.split(",", 1)[1] for s in signatures.split() if s.startswith("v1,")]
    return any(hmac.compare_digest(expected, c) for c in candidates)


def sign_webhook(msg_id: str, ts: int, raw_body: bytes, secret: str) -> str:
    """Solo para pruebas: genera el header webhook-signature."""
    key = base64.b64decode(secret.split("_", 1)[1])
    signed = f"{msg_id}.{ts}.".encode() + raw_body
    return "v1," + base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()
