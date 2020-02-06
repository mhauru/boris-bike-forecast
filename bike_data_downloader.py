import os
import logging
import requests
import zipfile
from urllib.parse import urlparse
from pathlib import Path


def download_file(datafolder, url):
    datafolder = Path(datafolder)
    datafolder.mkdir(parents=True, exist_ok=True)

    a = urlparse(url)
    filename = Path(os.path.basename(a.path))
    filepath = datafolder / filename
    # Don't redownload if we already have this file.
    if filepath.exists():
        logging.info("Already have {}".format(filename))
    else:
        logging.info("Downloading {}".format(filename))
        rqst = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(rqst.content)
    return filepath


logging.basicConfig(level=logging.INFO)
datafolder = Path("./data/bikes")

# Most files are individual CSV files, listed in bike_data_urls.txt. Download
# them.
urlsfile = "bike_data_urls.txt"
with open(urlsfile, "r") as f:
    urls = f.read().splitlines()
# There are a few comments in the file, marked by lines starting with #.
# Filter them out.
urls = [u for u in urls if u[0] != "#"]
for url in urls:
    download_file(datafolder, url)

# The early years come in zips. Download and unzip them.
zipsfolder = Path("./data/bikezips")
bikezipurls = [
    "http://cycling.data.tfl.gov.uk/usage-stats/cyclehireusagestats-2012.zip",
    "http://cycling.data.tfl.gov.uk/usage-stats/cyclehireusagestats-2013.zip",
    "http://cycling.data.tfl.gov.uk/usage-stats/cyclehireusagestats-2014.zip",
    "http://cycling.data.tfl.gov.uk/usage-stats/2015TripDatazip.zip",
    "http://cycling.data.tfl.gov.uk/usage-stats/2016TripDataZip.zip",
]
for url in bikezipurls:
    zippath = download_file(zipsfolder, url)
    logging.info("Unziping {}".format(zippath))
    with zipfile.ZipFile(zippath, "r") as z:
        z.extractall(datafolder)
