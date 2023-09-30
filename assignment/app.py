import requests
from bs4 import BeautifulSoup
import os, csv, time

import asyncio

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
async def get_html(link: str):
    # get page
    try:
        # res = requests.get("https://" + link)
        loop = asyncio.get_event_loop() # current event loop
        res = await loop.run_in_executor(
                None, requests.get, "https://%s" % link)
        # Here, event loop is created by
        # asyncio.run(main()) in the
        # script guard

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
    output_path = base_path + "/out/async10"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(output_path + f"/{sitename}.txt", "w") as outfile:
        outfile.write(title)


# TODO : convert to async
# scrape the given link synchronously
async def scrape(website: dict):
    os.system("") # enables ANSI escape sequences in terminal
    try:
        (html, err) = await get_html(website[DOMAIN_NAME])

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
async def main():
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

    tasks = [scrape({ SITE: site, DOMAIN_NAME: domain_name })
        for row in csvgen
        for (site, domain_name) in [row.strip().split(',')]
    ]

    loop = asyncio.get_event_loop() # current running event loop
    results = await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Completed tasks in {end - start} seconds")
