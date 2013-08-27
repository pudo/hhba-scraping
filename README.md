# Scraping Workshop for H/H BA

These code snippets are the core of a scraping workshop for the Hacks/Hackers Buenos 
Aires Media Party. It'd addressed at people who have already done some Python coding
but want to explore scraping in more depth.


## Setting up a working environment.

To recreate examples from the workshop, create a Python
[virtual environment](http://virtualenv.org/) like this:

    # Create the virtualenv:
    virtualenv scraping-env

    # Activate it:
    source scraping-env/bin/activate

    # Finally, install the dependencies for this workshop:
    pip install -r requirements.txt


## Topics

### Introduction 

* Getting started with Scraping in Python using [requests](http://docs.python-requests.org/en/latest/)
* Exploring HTML documents and extracting the data, with [lxml](http://lxml.de/parsing.html)
* Saving scraped data to a database with [dataset](http://dataset.rtfd.org/)
* Dealing with forms and searches.

### Advanced

* Dealing with sessions (e.g. logins)
* Running multiple requests in parallel to scrape faster
* Performing sanity checks on your data
* Understanding HTTP cache controls to check if new content is available.
* Hiding the fact that you're scraping a site 

### Pro

* Building your own [ScraperWiki](http://scraperwiki.com/) with [Jenkins CI](http://jenkins-ci.org/)
