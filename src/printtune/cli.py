"""Capability scanner command line interface."""
import argparse
import asyncio
import json
import os
from pathlib import Path

from .moonraker import MoonrakerClient


def main():
    parser = argparse.ArgumentParser(description="Read-only Klipper capability scan")
    parser.add_argument("--url", default=os.getenv("MOONRAKER_URL"))
    parser.add_argument("--output", default="capabilities.json")
    args = parser.parse_args()
    if not args.url:
        parser.error("Provide --url or MOONRAKER_URL")
    result = asyncio.run(MoonrakerClient(args.url, os.getenv("MOONRAKER_API_KEY")).discover())
    path = Path(args.output)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}. Review for sensitive information before sharing.")


if __name__ == "__main__":
    main()
