"""
cli.py — Command Line Interface entry point.
Accepts user arguments and calls the order placement logic.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 70000
"""
import argparse
import sys
import logging
from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import place_order, print_order_result

# ── Hardcoded for mock server demo
# Replace with userdata.get() or os.environ when using real testnet
API_KEY    = "test_key_123"
API_SECRET = "test_secret_456"


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --qty 0.01\n"
            "  python cli.py --symbol ETHUSDT --side SELL --type LIMIT  --qty 0.1 --price 3500\n"
        )
    )
    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair e.g. BTCUSDT, ETHUSDT"
    )
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", required=True, dest="order_type",
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "--qty", required=True, type=float,
        help="Order quantity e.g. 0.01"
    )
    parser.add_argument(
        "--price", required=False, type=float, default=None,
        help="Limit price (required for LIMIT orders)"
    )
    return parser


def main():
    """Main entry point — parse args, validate, place order."""
    setup_logging("trading_bot.log")
    logger = logging.getLogger(__name__)

    parser = build_parser()
    args   = parser.parse_args()

    logger.info(f"CLI called | symbol={args.symbol} side={args.side} "
                f"type={args.order_type} qty={args.qty} price={args.price}")

    # Validate LIMIT price early with helpful message
    if args.order_type == "LIMIT" and args.price is None:
        parser.error("--price is required when --type is LIMIT")

    # Connect
    try:
        client           = BinanceClient(API_KEY, API_SECRET)
        session, sign_fn = client.get_raw_session()
    except Exception as e:
        logger.error(f"Failed to initialise client: {e}")
        print(f"❌ Could not connect: {e}")
        sys.exit(1)

    # Place order
    try:
        result = place_order(
            session    = session,
            sign_fn    = sign_fn,
            symbol     = args.symbol,
            side       = args.side,
            order_type = args.order_type,
            quantity   = args.qty,
            price      = args.price
        )
        print_order_result(result, success=True)
        logger.info("Order placed successfully")
        sys.exit(0)

    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        print(f"\n❌ Invalid input: {e}")
        sys.exit(1)

    except RuntimeError as e:
        logger.error(f"Order failed: {e}")
        print(f"\n❌ Order failed: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
