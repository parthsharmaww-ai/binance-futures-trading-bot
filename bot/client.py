"""
client.py — Binance Futures client wrapper
Uses direct REST calls against mock server (or real testnet).
Change BASE_URL to switch between mock and real testnet.
"""
import hmac
import hashlib
import time
import logging
import requests
from urllib.parse import urlencode

BASE_URL = "http://localhost:8000"   # swap to testnet URL when available
logger = logging.getLogger(__name__)


class BinanceClient:

    def __init__(self, api_key: str, api_secret: str):
        self.api_key    = api_key
        self.api_secret = api_secret
        self.session    = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("BinanceClient initialised")

    def _sign(self, params: dict) -> dict:
        """Add timestamp + HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def ping(self) -> bool:
        """Check connectivity."""
        try:
            r = self.session.get(f"{BASE_URL}/fapi/v1/ping", timeout=10)
            r.raise_for_status()
            logger.info("Ping successful")
            return True
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            return False

    def get_balance(self) -> list:
        """Fetch non-zero account balances."""
        params = self._sign({})
        r = self.session.get(
            f"{BASE_URL}/fapi/v2/balance",
            params=params,
            timeout=10
        )
        r.raise_for_status()
        balances = r.json()
        non_zero = [b for b in balances if float(b["balance"]) > 0]
        logger.info(f"Balance fetched — {len(non_zero)} asset(s) found")
        return non_zero

    def get_raw_session(self):
        """Expose session and _sign for orders.py."""
        return self.session, self._sign
