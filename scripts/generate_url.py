from pathlib import Path
from typing import List
import logging


def generate_url(start: int, end: int) -> List[str]:
    """Generate url list"""
    parent = "https://www.trismegistos.org/text/"
    url_list = [f"{parent}{child}" for child in range(start, end+1)]
    logging.info(f"Generated {end - start + 1} urls, from {start} to {end}")
    return url_list


def main(output: Path, start: int, end: int) -> None:
    # Config logging
    logging.basicConfig(level=logging.DEBUG)
    # Generate url list
    url_list = generate_url(start, end)
    logging.info(f"Generated {len(url_list)} urls")
    # Output to file
    with open(output, "w") as f:
        for url in url_list:
            f.write(url + "\n")
    logging.info(f"Output to {output}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',
                        type=Path,
                        default=Path("../data/urls.txt"),
                        help="Output .txt file with one url per line")

    parser.add_argument('--start',
                        type=int,
                        default=601,
                        help="Start index of url.")

    parser.add_argument('--end',
                        type=int,
                        default=610,
                        help="End index of url.")

    args = parser.parse_args()

    # Check arguments
    if not args.output.suffix == ".txt":
        raise ValueError("Output file must end with .txt")

    main(output=args.output,
         start=args.start,
         end=args.end)
