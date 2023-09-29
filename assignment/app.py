import requests
from bs4 import BeautifulSoup
import os, csv, time

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
        # For some websites (e.g. Twitter): <link title="..." ... />
        for i in page.find_all("link"):
            if i.has_attr("title"):
                return i["title"]

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
    except Exception as e:
        return (None, Exception("Error!"))


# Writes to given title to file synchronously
def write_to_file(sitename: str, title: str):
    # TODO : write the title to a file in the /out directory named : <sitename>.txt
    # pass

    base_path = os.getcwd()
    output_path = base_path + "/out/sync6"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(output_path + f"/{sitename}.txt", "w") as outfile:
        outfile.write(title)


# TODO : convert to async
# scrape the given link synchronously
def scrape(website: dict):
    os.system("") # enables ANSI escape sequences in terminal
    try:
        (html, err) = get_html(website[DOMAIN_NAME])

        if err is not None:
            msg = website[SITE] + " : " + "FAILED!"
            # HINT : remember that -> writing to file is blocking
            # TODO : convert to async/threading?
            write_to_file(website[SITE], msg)
            # print(website[SITE], " : ", website[DOMAIN_NAME], "error!")
            print(website[SITE], " : ", website[DOMAIN_NAME], "\033[1;31merror!\033[m")
            return

        soup = BeautifulSoup(html, "html5lib")

        title = website[SITE] + " : TITLE -> " + get_title(soup)

        # TODO : convert to async/threading?
        write_to_file(website[SITE], title)
        # print(website[SITE], " : ", website[DOMAIN_NAME], "success!")
        print(website[SITE], " : ", website[DOMAIN_NAME], "\033[1;32msuccess!\033[m")

    except Exception as err:
        msg = website[SITE] + " : " + "FAILED!"
        # HINT : remember that -> writing to file is blocking
        # TODO : convert to async/threading?
        write_to_file(website[SITE], msg)
        # print(website[SITE], " : ", website[DOMAIN_NAME], "error!")
        print(website[SITE], " : ", website[DOMAIN_NAME], "\033[1;31merror!\033[m")


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

    csvgen = (row for row in open(dataset_path, "r"))
    next(csvgen) # to skip header row

    for row in csvgen:
        site, domain_name = row.strip().split(',')
        scrape({ SITE: site, DOMAIN_NAME: domain_name })


start = time.time()
main()
end = time.time()
print(f"Completed tasks in {end - start} seconds")
