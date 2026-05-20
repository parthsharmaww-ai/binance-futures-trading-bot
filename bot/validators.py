"""
validators.py — Input validation before any order is sent.
Catches bad inputs early so we never send garbage to the API.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_order(symbol: str, side: str, order_type: str,
                   quantity: float, price: float = None) -> None:
    """
    Validate all order inputs.
    Raises ValueError with a clear message if anything is wrong.
    """

    # Symbol
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string e.g. BTCUSDT")
    if not symbol.endswith("USDT"):
        raise ValueError(f"Symbol '{symbol}' must end with USDT e.g. BTCUSDT")

    # Side
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got '{side}'")

    # Order type
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be MARKET or LIMIT, got '{order_type}'")

    # Quantity
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError(f"Quantity must be a positive number, got '{quantity}'")

    # Price — only required for LIMIT orders
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f"Price must be a positive number, got '{price}'")

    if order_type.upper() == "MARKET" and price is not None:
        raise ValueError("Price should not be set for MARKET orders")
