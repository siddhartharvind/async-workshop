# Specification Document for Async Workshop Project - Hands On

## Specification

What the program is meant to do?

Given program is meant to take the given dataset of csv with : Site,Domain Name
and scrape (web) it to get the webpage. We then get the title of the website and
write it to file.

Functions and what they do :

`get_title` : function that will take the beautiful soup object and get the
title of the page

`get_html` : makes a GET request using the appropriate library and returns the
html and error

`write_to_file` : writes the given message synchronously to a file named
<sitename>.txt in the out directory

`scrape` : function takes the website details and performs the scraping, if any
errors are thrown during the process, fail message is written to file, else a
success and title of web page as message is written to file

`main` : reads from the csv file and calls the scrape function on each of the
links provided in the dataset

## Instructions

Given to you is an incomplete synchronous version. Some of the boilerplate code
is written to help you get started.

1. Fork the given git repository

2. Install required libraries using :

```
pip3 install -r requirements.txt
```

To install other libraries use :

```
pip3 install <libname>
```

(or)

```
pip install <libname>
```

3. Check the TODO items from the comments written in the boilerplate code and
   make the changes accordingly. Use the internet to search for clues and
   documentation!

4. If you're done or have any doubts, contact us!

## Random Bits/Facts to keep in mind

-   The CSV dataset has the following columns : Site,Domain Name
-   BeautifulSoup and html5lib to parse the html and give us a usable interface
-   Writing to files is blocking
-   Be wary of where you use `async` to make a synchronous python function
    asynchronous
