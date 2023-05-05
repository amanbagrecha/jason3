"""
Code adapted from https://github.com/fraymio/modis-tools
Creates a session to authenticate earthdata
"""
from urllib.parse import urlsplit
from requests.auth import HTTPProxyAuth, HTTPBasicAuth
from requests import sessions


class JasonSession:
    """Auth session for querying and downloading Jason-3 data."""

    session: sessions.Session

    def __init__(
        self,
        username=None,
        password=None,
        auth=None,
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
