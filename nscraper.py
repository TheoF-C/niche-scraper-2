import time
import requests
from bs4 import BeautifulSoup
from page_paths import PATHS


class NScraper:
    """web scraper for getting college data off niche.com"""

    def __init__(self, headers, page_lim=111, delay=7):
        self.HEADERS = headers
        self.PAGE_LIM = page_lim
        self.DELAY = delay
        self.data = {}

    def compile_colleges(self, pages=None, start=1) -> None:
        """compiles colleges off of Niche's best-colleges page and adds the names to self.data"""

        if pages is None:
            pages = self.PAGE_LIM

        url = "https://www.niche.com/colleges/search/best-colleges/"

        for i in range(start, pages + 1):
            response = requests.get(url, headers=self.HEADERS, params=(('page', str(i)),))
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all("li", {"class": "search-results__list__item"})
            names = [college.find("section")["aria-label"] for college in results]
            locations = [college.find_all("li", {"class": "search-result-tagline__item"})[1].text for college in
                         results]
            self.add_colleges(names, locations)
            time.sleep(self.DELAY)

    def scrape(self, actions: list, data=None, sync=False, thread=None) -> None:
        """
        scrapes data according to actions parameter off of colleges according to the colleges parameter
        the colleges parameter will use colleges in self.data by default (still needs to be implemented)
        sync adjusts time delay for operation time in during the scrape (needs testing)
        thread allows a function to be passed to be executed during delay time
        """
        if data is None:
            data = self.data
        else:
            self.add_colleges(data)

        base_url = "https://www.niche.com/colleges/"

        for college, value in data.items():
            response = requests.get(base_url + college, headers=self.HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            start = time.perf_counter()

            for action in actions:
                if action == "popular_majors":
                    majors = self.subject_scrape(soup)
                    for i in range(len(majors)):
                        value[f"major_{i}_name"] = majors[i][0]
                        value[f"major_{i}_value"] = majors[i][1]
                try:

                    pass
                    value[action] = self.bucket_scrape(soup, PATHS[action][0], PATHS[action][1])
                except AttributeError:
                    value[action] = None
                    print(college + ":")
                    print(f'error {action} not found')

            self.data[college] = self.format_data(value)

            if thread is not None:
                thread(value)

            if sync:
                time.sleep(self.DELAY - round(time.perf_counter() - start, 2))
            else:
                time.sleep(self.DELAY)

    @staticmethod
    def bucket_scrape(soup, eid: str, label: str):
        """helper function to self.scrape responsible for finding data point given PATHS address"""

        # locates bucket where the data is stored
        soup = soup.find(id=eid).find("div", {"class": "profile__buckets"}).find_all("span")
        heated_soup = None

        # searches through 'spans' within bucket to find data
        for span in soup:
            if span and span.text == label:
                heated_soup = span.parent.find_next_sibling()
                break

        if heated_soup is not None:
            return heated_soup.find("span").text

        return None

    @staticmethod
    def subject_scrape(soup):
        soup = soup.find(id="majors").find_all("li", {"class": "popular-entities-list-item"})
        majors = [[college.find("div", {"class": "popular-entity__name"}).text,
                   college.find("div", {"class": "popular-entity-descriptor"}).text] for college in soup[:3]]
        if len(majors) < 3:
            majors += [None] * (3 - len(majors))
        return majors

    @staticmethod
    def format_data(data: dict) -> dict:
        """formats and cleans college data"""

        def format_score(type):
            key = type + "_range"
            if key in data and data[key] is not None:
                score_range = data[key].split("-")
                data[type + "_low"] = int(score_range[0])
                data[type + "_high"] = int(score_range[1])
                del data[key]

        for key in data:
            if data[key] == 'No data available \xa0':
                data[key] = None
            elif isinstance(data[key], str):
                processed = data[key].translate({ord(c): None for c in "$%,"})
                if processed.isdigit():
                    data[key] = int(processed)

        format_score("sat")
        format_score("act")
        return data

    def format_all(self) -> None:
        """runs self.format_data on all colleges stored in self.data"""
        for college in self.data:
            self.format_data(self.data[college])

    @staticmethod
    def process_name(name: str) -> str:
        """processes college names into names suitable for using in url"""
        return '-'.join(name.lower().split()).replace('&', '-and-').replace('SUNY', 'suny').translate(
            {ord(c): None for c in "().,'"})

    def get_colleges(self) -> list:
        """returns a list of all colleges stored in self.data"""
        return list(self.data.keys())

    def add_colleges(self, colleges: list, locations=None) -> None:
        """adds colleges to self.data"""
        for i, college in enumerate(colleges):
            self.data[self.process_name(college)] = {'name': college,
                                                     'area': locations[i][:-5].title() if locations else None,
                                                     'state': locations[i][-3:-1] if locations else None}

    def del_colleges(self, colleges: list) -> None:
        """deletes colleges from self.data"""
        for college in colleges:
            del self.data[college]
