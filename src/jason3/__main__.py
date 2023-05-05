"""
This scripts helps download Jason-3 (jason3) data through CMR API
Those jason3 passes which intersects the bounds, are completely downloaded
"""

import argparse
from jason3 import process


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default=".nc",
        help="File extension to avoid ",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Earthdata Username - If not registered, create account here https://urs.earthdata.nasa.gov/",
        required=True,
    )
    parser.add_argument(
        "-p", "--password", type=str, help="Earthdata Password", required=True
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=".",
        help="Output directory",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--concept_id",
        type=str,
        default="C2205122298-POCLOUD",
        help="Collection concept ID taken from https://cmr.earthdata.nasa.gov/search/site/collections/directory/POCLOUD/gov.nasa.eosdis",
        required=True,
    )
    parser.add_argument(
        "-b",
        "--bbox",
        type=str,
        default="0,-5,5,0",
        help="Bounding box with format `xmin, ymin, xmax, ymax`",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--temporal",
        type=str,
        default="2022-01-01T10:00:00Z,2022-01-02T12:00:00Z",
        help="Temporal range",
        required=True,
    )
    parser.add_argument(
        "-l", "--page_size", type=int, default=2, help="Page size", required=True
    )

    try:
        args = parser.parse_args()
    except:
        raise SystemExit()

    username = args.username
    password = args.password
    output_dir = args.output_dir
    extension = args.extension
    params = dict(
        collection_concept_id=args.concept_id,
        bounding_box=args.bbox,
        temporal=args.temporal,
        page_size=args.page_size,
    )

    process.download(params, username, password, extension, output_dir)


if __name__ == "__main__":
    main()
