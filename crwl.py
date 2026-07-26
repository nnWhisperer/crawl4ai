"""Compatibility dispatcher for the full and remote Crawl4AI CLIs."""

import sys


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "remote":
        from crwl_remote import main as remote_main
        remote_main()
        return

    from crawl4ai.cli import main as local_main
    local_main()


if __name__ == "__main__":
    main()
