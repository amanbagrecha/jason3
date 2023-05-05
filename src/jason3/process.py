import requests
import os
from jason3 import session, URL

# To download data from cmr, after filtering the granule,
# we need to find the link to download (with.nc)


def write_file(obj, attributes, output_dir):
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
            print("get() returned an error code " + str(r.status_code))


def download(params, username, password, extension, output_dir):
    obj = session.JasonSession(username, password)
    resp = requests.get(URL, params=params)
    resp_json = resp.json()
    resp_list = resp_json["feed"]["entry"]
    attributes = []

    for i in resp_list:
        for j in i["links"]:
            if j["href"].startswith("https") & j["href"].endswith(extension):
                attributes.append(j["href"])

    if attributes:
        print(
            f"Downloading {len(attributes)} files to {output_dir} output dir with {params}"
        )

    write_file(obj, attributes, output_dir)
