from bs4 import BeautifulSoup
from selenium import webdriver
import json

class Scraper:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Scraper, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.URL = "https://www.sciente.com/business-technology-jobs/"
        self.scraped = 0

    def __soupify(self, url: str) -> BeautifulSoup:
        driver = self.driver
        driver.get(url)
        content = driver.execute_script("return document.body.innerHTML")
        return BeautifulSoup(content, 'html.parser')

    def __info_list(self, soup: BeautifulSoup, text: str) -> list[str]:
        element = soup.find('b', string=text)
        element = element.parent.next_sibling.next_sibling
        if not element:
            return []
        return [li.text.strip() for li in element.find_all('li')]

        
    def __get_job_info(self, job: BeautifulSoup) -> dict[str, str | list[str]]:
        link = str(job.get('href'))
        listing = self.__soupify(link)
        body = listing.find('div', class_="single-entry-body")
        result = {
            "title": listing.find('div', class_="single-entry-title").find('h2').text.strip(),
            "description": body.find('p').text.strip(),
            **{key: self.__info_list(body, key) for key in ["Mandatory Skill(s)", "Desirable Skill(s)", "Responsibilities"]}
        }
        return result

    def __next_page(self, soup: BeautifulSoup) -> BeautifulSoup | None:
        next_button = soup.select(".next.page-numbers")
        if next_button:
            link = next_button[0].get('href')
            return self.__soupify(link)
        return None

    def scrape(self) -> list[dict[str, str | list[str]]]:
        soup = self.__soupify(self.URL)
        job_data = []
        while soup:
            jobs = soup.find('div', class_="wdt-posts-list-wrapper").find_all('a', class_="wdt-button")

            for job in jobs:
                job_info = self.__get_job_info(job)
                job_info["id"] = len(job_data)
                job_data.append(job_info)
                print(f'#{job_info["id"]} {job_info["title"]}')

            soup = self.__next_page(soup)
        self.scraped = len(job_data)
        print(f"Scraped {self.scraped} jobs")

        with open('recruitment/services/scraper/files/scrape.txt', 'w') as f:
            json.dump(job_data, f, indent=4)
        with open('recruitment/services/scraper/files/scrape.json', 'w') as f:
            json.dump(job_data, f, indent=4)
        print("Saved to scrape.txt and scrape.json")
        return job_data

if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()




