# Niche Scraper

Niche.com is a website showing profiles of schools across the U.S. The data on Niche is a comprehensive compilation of public data, surveys, and reviews. The aim of this project is to provide a simple webscraper (nscraper.py) for accumulating data found on Niche. While the project is currently configured to get data on colleges, it could be easily modified to scrape highschool or K-12 data.

## Usage

First, initiliatize the NScraper object. In this case the scraper is created with the headers from config.py and a delay of 5 seconds. The header includes your user agent and the delay specifies the wait time before switching pages, which are both necessary in order to not get denied from the page.

```python
nScraper = NScraper(config.HEADERS, delay=5)
```

Next, start compiling college names. While this step is not necessary if you already have college names to give the scraper, this function will automatically compile and add college names off of Niche's best colleges page.

In this example, it starts compiling at page 1 and goes for 10 pages.

```python
nScraper.compile_colleges(start=1, pages=10)
```

Start the scrape after the names have compiled. ACTIONS dictates what data the scraper gets. Actions can be added, removed, or modified depending on the target data.

```python
nScraper.scrape(actions=ACTIONS)
```

## Actions

The scraper performs an action to get the desired piece of data. This action shows the graduation rate.

```python
"graduation_rate"      :       [0, "after", "Graduation Rate"]
```

The "0" is the action type, which in this case is bucket scrape. Niche's profiles are made up of 'buckets', and the "after" and "Graduation Rate" instructions are saying grab the graduation rate data from the "after" bucket.

There are also action types 1, 2, and 3, which are for location, major, and test scores respectively.

## main.py

This is a detailed example of how nscraper works and can be used with other programs. Google Places API is used to aproximate coordinates from the college name and location.
