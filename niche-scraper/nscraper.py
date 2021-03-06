import time
import requests
from bs4 import BeautifulSoup
from page_actions import ACTIONS
from college import College


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

        url = "https://webcache.googleusercontent.com/search?q=cache:https://www.niche.com/colleges/search/best-colleges/"

        for i in range(start, pages + 1):
            response = requests.get(url, headers=self.HEADERS, params=(('page', str(i)),))
            print(response)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all("li", {"class": "search-results__list__item"})
            names = [college.find("section")["aria-label"] for college in results]
            self.add_colleges(names)
            time.sleep(self.DELAY)

    def scrape(self, actions: list, data=None, thread=None) -> None:
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

        base_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.niche.com/colleges/"

        for college_name, college in data.items():
            response = requests.get(base_url + college_name, headers=self.HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')

            for action in actions:
                instruction = ACTIONS[action][0]

                if instruction == 0:  # general
                    college.add_data(action, self.bucket_scrape(soup, ACTIONS[action][1], ACTIONS[action][2]))
                elif instruction == 1:  # location
                    college.add_location(self.location_scrape(soup))
                elif instruction == 2:  # majors
                    college.add_major(self.major_scrape(soup, ACTIONS[action][1]))
                elif instruction == 3:  # scores
                    college.add_score(action, self.bucket_scrape(soup, ACTIONS[action][1], ACTIONS[action][2]))

            if thread is not None:
                thread(college.data)

            time.sleep(self.DELAY)

    @staticmethod
    def bucket_scrape(soup, eid: str, label: str):
        """helper function to self.scrape responsible for finding data point given PATHS address"""

        # locates bucket where the data is stored
        if soup.find(id=eid) is None:
            print(soup)

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
    def location_scrape(soup):
        return soup.find_all("li", {"class": "postcard__attr postcard-fact"})[1].text

    @staticmethod
    def major_scrape(soup, amount):
        soup = soup.find(id="majors").find_all("li", {"class": "popular-entities-list-item"})
        majors = [[college.find("div", {"class": "popular-entity__name"}).text,
                   college.find("div", {"class": "popular-entity-descriptor"}).text] for college in soup[:amount]]
        if len(majors) < amount:
            majors += [None] * (amount - len(majors))
        return majors

    @staticmethod
    def process_name(name: str) -> str:
        """processes college names into names suitable for using in url"""
        return '-'.join(name.lower().split()).replace('&', '-and-').replace('SUNY', 'suny').translate(
            {ord(c): None for c in "().,'"})

    def get_colleges(self) -> list:
        """returns a list of all colleges stored in self.data"""
        return list(self.data.keys())

    def add_colleges(self, colleges: list) -> None:
        """adds colleges to self.data"""
        for college in colleges:
            self.data[self.process_name(college)] = College(college)

    def del_colleges(self, colleges: list) -> None:
        """deletes colleges from self.data"""
        for college in colleges:
            del self.data[college]
