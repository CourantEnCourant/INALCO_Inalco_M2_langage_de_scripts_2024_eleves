from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from typing import List, Tuple, Dict
import logging

content2xpath = {
    'date': '//*[@id="text-details"]/div',
    'provenance': '//*[@id="text-details"]/p[1]/*[position()>1]',
    'material': '//*[@id="text-details"]/p[3]/*[position()>1]',
    'content': '//*[@id="text-details"]/p[5]',
    'publications': '//*[@id="text-publs"]/*[position()>1]',
    'collections': '//*[@id="text-coll"]/*[position()>1]',
    'archive': '//*[@id="text-arch"]/*[position()>1]',
    'full_text': '//*[@id="words-full-text"]/*'
}

section2button = {
    'people': '//*[@id="people-header-text"]',
    'places': '//*[@id="places-header-text"]',
    #'irregularities': '//*[@id="textirr-header-text"]'
}

section2xpath = {
    'people': '//*[@id="people-list"]//li[@class="item-large ui-corner-left"]',
    'places': '//*[@id="places-list"]//li[@class="item-large ui-corner-left"]',
    'irregularities': '//*[@id="texirr-list"]//li[@class="item-large ui-corner-left"]'
}


def get_text_concat(driver: WebDriver, xpath: str) -> str:
    elements = driver.find_elements(By.XPATH, xpath)
    return "".join([element.text for element in elements])


def scrap_papyrus(url: str, driver: WebDriver) -> dict:
    driver.get(url)
    page = {}

    # Information stored as `str`
    for key, xpath in content2xpath.items():
        page[key] = get_text_concat(driver, xpath)
        if not page[key]:
            logging.warning(f"Got empty string for {key}, scrapping may have partially failed on page {url}")

    # Information stored as `List[str]`
    for section, xpath in section2xpath.items():
        section_element_list = driver.find_elements(By.XPATH, xpath)
        section_text_list = [element.text for element in section_element_list]
        page[section] = section_text_list

    return page


def main():
    driver = webdriver.Chrome(service=Service())
    driver.implicitly_wait(5)
    scrap_papyrus(url='https://www.trismegistos.org/text/103', driver=driver)


if __name__ == '__main__':
    main()
