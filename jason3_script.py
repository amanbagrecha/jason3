"""
Code adapted from https://github.com/fraymio/modis-tools

This scripts helps download Jason-3 (jason3) data through CMR API
Those jason3 passes which intersects the bounds, are completely downloaded
"""
import argparse
from urllib.parse import urlsplit
from requests.auth import HTTPProxyAuth

from requests import sessions
from requests.auth import HTTPBasicAuth
import requests
import os

URL = "https://cmr.earthdata.nasa.gov/search/granules.json"


class JasonSession:
    """Auth session for querying and downloading Jason-3 data."""

    session: sessions.Session

    def __init__(
        self, username=None, password=None, auth=None,
    ):
        self.username = username
        self.password = password
        self.session = sessions.Session()
        if auth:
            self.session.auth = auth
        elif username is not None and password is not None:
            self.session.auth = HTTPBasicAuth(username, password)

    def get_location(self, url):
        """Make initial request to fetch file location from header."""
        session = self.session
        split_result = urlsplit(url)
        https_url = split_result._replace(scheme="https").geturl()
        location_resp = session.get(https_url, allow_redirects=False)
        if location_resp.status_code == 401:
            # try using ProxyAuth if BasicAuth returns 401 (unauthorized)
            location_resp = session.get(
                https_url,
                allow_redirects=False,
                auth=HTTPProxyAuth(self.username, self.password),
            )
        location = location_resp.headers.get("Location")
        if not location:
            raise FileNotFoundError("No file location found")
        return location


parser = argparse.ArgumentParser()
parser.add_argument('-e', "--ext", type=str, default=".nc", help="File extension")
parser.add_argument("-u", "--username", type=str,default='####',  help="Username")
parser.add_argument("-p", "--password", type=str, default='####', help="Password")
parser.add_argument('-o', "--output_dir", type=str, default=".", help="Output directory")
parser.add_argument('-c', "--concept_id", type=str, default="C2205122298-POCLOUD", help="Collection concept ID")
parser.add_argument('-b',"--bbox", type=str, default="0,-5,5,0", help="Bounding box")
parser.add_argument('-t', "--temporal", type=str, default="2022-01-01T10:00:00Z,2022-01-02T12:00:00Z", help="Temporal range")
parser.add_argument('-l', "--page_size", type=int, default=2, help="Page size")

args = parser.parse_args()


if __name__ == "__main__":

    username = args.username
    password = args.password
    output_dir = args.output_dir
    params = dict(
        collection_concept_id=args.concept_id,
        bounding_box=args.bbox,
        temporal=args.temporal,
        page_size=args.page_size,
    )

    if not username or not password:
        raise Exception("Either credentials are not passed")

    # To download data from cmr, after filtering the granule,
    # we need to find the link to download (with.nc)
    resp = requests.get(URL, params=params)
    resp_json = resp.json()
    resp_list = resp_json["feed"]["entry"]
    attributes = []

    for i in resp_list:
        for j in i["links"]:
            if j["href"].startswith("https") & j["href"].endswith(".nc"):
                attributes.append(j["href"])

    if attributes:
        print(
            f"Downloading {len(attributes)} files to {output_dir} output dir with {params}"
        )

    obj = JasonSession(username, password)

    for _url in attributes:
        response_302 = obj.get_location(_url)
        r = obj.session.get(response_302, allow_redirects=True)
        try:
            r.raise_for_status()
            filename = os.path.join(output_dir, f'{_url.split("/")[-1]}')
            with open(filename, "wb") as f:
                f.write(r.content)
                print(f"Downloaded {filename}")
        except:
            print('get() returned an error code '+str(r.status_code))

