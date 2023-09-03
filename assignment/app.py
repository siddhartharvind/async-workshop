import requests
from bs4 import BeautifulSoup
import os, csv, time

from pathlib import Path    # to handle Windows/Unix filepaths

"""
Assignment Instructions : 

1. Install BeautifulSoup, requests using :

pip3 install bs4
pip3 install requests

2. Some of the boilerplate code is written to help you get started.
Check the TODO items and make the changes accordingly

3. If you're done contact us!
"""

# KEYS
DOMAIN_NAME = "Domain Name"
SITE = "Site"


# Get title from the parsed html
def get_title(page: BeautifulSoup):
    title = page.find("title")
    if title is not None:
        return title.get_text()
    else:
        raise Exception("nah")


# TODO : convert to async
# Gets the html by making a GET request to given URL
def get_html(link: str):
    # get page
    try:
        res = requests.get("https://" + link)

        if res is not None:
            return (res.content.decode("utf-8"), None)
        else:
            return (None, Exception("No html!"))
    except:
        return (None, Exception("Error!"))


# Writes to given title to file synchronously
def write_to_file(sitename: str, title: str):
    # TODO : write the title to a file in the /out directory named : <sitename>.txt
    # pass

    # base path
    base_path = os.getcwd()

    # Make sure spaces in sitename are handled
    # file_path = "{}/out/sync/{}.txt".format(base_path, sitename)
    folder_path = Path("./out/sync/")
    folder_path.mkdir( parents=True, exist_ok=True ) # create subfolder 'sync' if not exists

    file_path = folder_path / sitename 

    with open(file_path, "w") as output_file:
        output_file.write(title)


# TODO : convert to async
# scrape the given link synchronously
def scrape(website: dict):
    try:
        (html, err) = get_html(website[DOMAIN_NAME])

        if err is not None:
            msg = website[SITE] + " : " + "FAILED!"
            # HINT : remember that -> writing to file is blocking
            # TODO : convert to async/threading?
            write_to_file(website[SITE], msg)
            print(website[SITE], " : ", website[DOMAIN_NAME], "error!")
            return

        soup = BeautifulSoup(html, "html5lib")

        title = website[SITE] + " : TITLE -> " + get_title(soup)

        # TODO : convert to async/threading?
        write_to_file(website[SITE], title)
        print(website[SITE], " : ", website[DOMAIN_NAME], "success!")

    except Exception as err:
        msg = website[SITE] + " : " + "FAILED!"
        # HINT : remember that -> writing to file is blocking
        # TODO : convert to async/threading?
        write_to_file(website[SITE], msg)
        print(website[SITE], " : ", website[DOMAIN_NAME], "error!")


# TODO : convert to async
def main():
    # print the process id
    print("PROCESS ID : ", os.getpid())
    time.sleep(2)

    # base path
    base_path = os.getcwd()

    dataset_path = base_path + "/dataset/websites.csv"

    # TODO : convert to async
    # TODO : read csv of links in dictionary format
    # TODO : call the scrape function on them one by one
    with open(dataset_path) as csvfile:
        csvDictReader = csv.DictReader(csvfile)

        for site_dict in csvDictReader:
            scrape(site_dict)


if __name__ == "__main__":
    main()
