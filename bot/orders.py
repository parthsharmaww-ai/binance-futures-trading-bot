"""
orders.py — Order placement with full error handling and logging.
"""
import logging
import requests
from urllib.parse import urlencode
from bot.validators import validate_order

BASE_URL = "http://localhost:8000"
logger = logging.getLogger(__name__)


def place_order(session, sign_fn, symbol: str, side: str,
                order_type: str, quantity: float, price: float = None) -> dict:
    """
    Place a MARKET or LIMIT order with full error handling.
    Returns a clean result dict.
    Raises ValueError for bad inputs, RuntimeError for API failures.
    """

    # Step 1 — Sanitize inputs
    symbol     = symbol.strip().upper()
    side       = side.strip().upper()
    order_type = order_type.strip().upper()

    # Step 2 — Validate
    try:
        validate_order(symbol, side, order_type, quantity, price)
    except ValueError as e:
        logger.warning(f"Validation failed: {e}")
        raise

    # Step 3 — Build params
    params = {
        "symbol":   symbol,
        "side":     side,
        "type":     order_type,
        "quantity": quantity,
    }
    if order_type == "LIMIT":
        params["price"]       = price
        params["timeInForce"] = "GTC"

    # Step 4 — Log request
    logger.info(f"ORDER REQUEST | {symbol} | {side} | {order_type} "
                f"| qty={quantity}" + (f" | price={price}" if price else ""))

    # Step 5 — Print request summary
    print(f"\n{'='*48}")
    print(f"  📤 ORDER REQUEST SUMMARY")
    print(f"{'='*48}")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print(f"{'='*48}")

    # Step 6 — Sign and send
    try:
        signed_params = sign_fn(params)
        r = session.post(
            f"{BASE_URL}/fapi/v1/order",
            data=signed_params,
            timeout=10
        )
        r.raise_for_status()

    except requests.exceptions.Timeout:
        msg = "Request timed out — Binance API not responding"
        logger.error(msg)
        raise RuntimeError(msg)

    except requests.exceptions.ConnectionError:
        msg = "Connection error — check your internet connection"
        logger.error(msg)
        raise RuntimeError(msg)

    except requests.exceptions.HTTPError as e:
        msg = f"API HTTP error: {e} | Response: {r.text}"
        logger.error(msg)
        raise RuntimeError(msg)

    # Step 7 — Parse response
    try:
        response = r.json()
    except Exception:
        msg = f"Could not parse API response: {r.text}"
        logger.error(msg)
        raise RuntimeError(msg)

    # Step 8 — Log response
    logger.info(f"ORDER RESPONSE | orderId={response.get('orderId')} "
                f"| status={response.get('status')} "
                f"| executedQty={response.get('executedQty')} "
                f"| avgPrice={response.get('avgPrice')}")

    # Step 9 — Build clean result
    result = {
        "orderId":     response.get("orderId"),
        "symbol":      response.get("symbol"),
        "side":        response.get("side"),
        "type":        response.get("type"),
        "status":      response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice":    response.get("avgPrice"),
    }

    return result


def print_order_result(result: dict, success: bool = True) -> None:
    """Print a clean formatted order result."""
    print(f"\n{'='*48}")
    print(f"  {'✅ ORDER SUCCESS' if success else '❌ ORDER FAILED'}")
    print(f"{'='*48}")
    print(f"  Order ID     : {result.get('orderId')}")
    print(f"  Symbol       : {result.get('symbol')}")
    print(f"  Side         : {result.get('side')}")
    print(f"  Type         : {result.get('type')}")
    print(f"  Status       : {result.get('status')}")
    print(f"  Executed Qty : {result.get('executedQty')}")
    print(f"  Avg Price    : {result.get('avgPrice')}")
    print(f"{'='*48}")
