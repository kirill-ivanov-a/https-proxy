import argparse
import socket

__all__ = ["parse_args"]

from proxy import HttpProxy


def parse_args() -> argparse.Namespace:
    def positive_int(value: str) -> int:
        try:
            value = int(value)
            if value <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
        except ValueError as error:
            raise argparse.ArgumentTypeError(f"{value} is not an integer") from error
        return value

    parser = argparse.ArgumentParser(
        prog="python -m proxy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=run_proxy)
    parser.add_argument(
        "--host",
        type=str,
        metavar="HOST",
        help="host to listen",
        default="0.0.0.0"

    )
    parser.add_argument(
        "--port",
        "-p",
        type=positive_int,
        metavar="PORT",
        help="port to listen",
        default=9000,
    )

    return parser.parse_args()


def run_proxy(args: argparse.Namespace):
    try:
        HttpProxy(
            host=args.host,
            port=args.port,
        ).run()
    except PermissionError:
        print("Operation not permitted")
    except socket.error as e:
        print(f"Unable to bind to the host {args.host}:{args.port}: {e}")
    except KeyboardInterrupt:
        print("Stopped...")
