import os
import sys
import glob
import urllib.request
import gdown
import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime

# Constant for specifying the location to place all the financial reports
DOWNLOAD_DIR = "reports"


## Read-in county argument from command-line (if it exists)
process_county = False
first_county = None
if len(sys.argv) > 1:
    first_county = sys.argv[1]
else:
    process_county = True

### Setup logging
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H-%M-%S")

logger = logging.getLogger()
handler = logging.FileHandler(mode="w", filename="logs" + date_time + ".txt")
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def getFinancialReportFilename(linkText):
    result = re.search(r"([A-Z\s]+).*(\d+)/(\d+)/(\d+)", linkText)
    filename = "TX FINANCIAL REPORT " + result.groups()[3] + ".pdf"
    return filename


def download_file(download_url, file_url):
    response = urllib.request.urlopen(download_url)
    file = open(file_url, "wb")
    file.write(response.read())
    file.close()


def contains_file(directory, filename):
    created_files = os.listdir(directory)
    found = False
    for created_file in created_files:
        if created_file == filename:
            found = True
    return found


def parseDistrict(districtLink, countyLink):
    logging.info("   %s", districtLink.text)
    directory = (
        DOWNLOAD_DIR + "\\" + countyLink.text + "\\" + districtLink.text.strip() + "\\"
    )
    os.makedirs(directory, exist_ok=True)
    r = requests.get(districtLink["href"])
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", "fusion-button")
    for link in links:
        if "FINANCIAL REPORT" in link.text or "FINANCIAL AUDIT" in link.text:
            if link["href"] == "#":
                logging.warning("      Invalid link for: " + link.text)
                continue
            filename = getFinancialReportFilename(link.text)
            if contains_file(directory, filename):
                logging.info("      %s -- ALREADY EXISTS", filename)
                continue
            file_path = directory + filename
            file_url = (
                link["href"]
                .replace("view?usp=sharing", "")
                .replace("file/d/", "uc?id=")
                .replace("/open", "/uc")
            )
            if len(file_url) > 0 and file_url[0] == "#":
                file_url = file_url[1:]
            shortened_url = file_url[: len(file_url) - 1]
            gdown.download(shortened_url, file_path)
            if contains_file(directory, filename):
                logging.info("      %s -- ADDED", filename)
            else:
                logging.info("      %s -- MISSING", filename)


def parseCounty(link):
    logging.info("%s", link.text)
    r = requests.get(link["href"])
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", "fusion-button")
    for districtLink in links:
        parseDistrict(districtLink, link)
    logging.info("   ")


r = requests.get("https://www.districtdirectory.org/")

soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all("a", "fusion-button")
count = 0
for link in links:
    # print(link['href'])
    if process_county:
        parseCounty(link)
    else:
        if first_county.lower() in link.text.lower():
            process_county = True
            parseCounty(link)
        else:
            logging.info("%s -- SKIPPED", link.text)
