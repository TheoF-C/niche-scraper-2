import config
import csv
import requests
import json
import lxml.html

from nscraper import NScraper
from page_actions import ACTIONS

api_key = config.API_KEY

FIELDS = [
    "name",
    "area",
    "state",
    "acceptance",  # %
    "deadline",  # Date
    "application fee",  # $
    "sat/act_required",
    "gpa_required",
    "early_decision",
    "common_app",
    "cost",  # $
    "aid_amount",  # $
    "aid_percent",  # %
    "enrollment",
    "part_time_undergrads",
    "undergrads_over_25",  # %
    "pell_grant",  # %
    "varsity_athletes",  # %
    "freshman_on_campus",  # %
    "median_earnings_after_6_years",  # $ / Year
    "graduation_rate",  # %
    "employed_2_years_after",
    "major_1",
    "major_2",
    "major_3",
    "sat_low",  # Score Range
    "sat_high",  # Score Range
    "act_low",  # Score Range
    "act_high",  # Score Range
    "latitude",
    "longitude"
]


def get_proxies():
    url = 'https://free-proxy-list.net/'

    response = requests.get(url)
    parser = lxml.html.fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)

    return proxies


def write_header():
    with open("data_main.csv", 'a') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(FIELDS)
    csvfile.close()


def get_coords(row):
    auto_url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?"
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json?"

    try:
        college = row['name']
        college = college.replace(" ", "+")

        auto_r = requests.get(f'{auto_url}input={college},%20{row["area"]},%20{row["state"]}&key={api_key}')
        auto_r = json.loads(auto_r.text)
        predicted = auto_r["predictions"][0]["place_id"]

        geo_r = requests.get(geo_url + 'place_id=' + predicted + '&key=' + api_key)
        geo_r = json.loads(geo_r.text)

        result = geo_r["results"][0]["geometry"]["location"]
        row['latitude'] = result['lat']
        row['longitude'] = result['lng']

    except (KeyError, IndexError):
        row['latitude'] = None
        row['longitude'] = None


def main():

    write_header()

    nScraper = NScraper(config.HEADERS, delay=5)

    print("-----------------------")
    print("compiling colleges.")
    print("-----------------------")

    for i in range(1):
        i += 50
        nScraper.compile_colleges(start=i, pages=i)
        try:
            print(f'page {i} loaded.')
        except Exception:
            print(f'error on page {i}.')

    print("-----------------------")
    print("processing colleges.")
    print("-----------------------")

    print(nScraper.get_colleges())

    def process(value):
        print(f'{value["name"]} loading.')
        get_coords(value)
        with open("data_main.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=value.keys())
            writer.writerow(value)
        csvfile.close()

    nScraper.scrape(actions=ACTIONS, thread=process)


if __name__ == "__main__":
    main()