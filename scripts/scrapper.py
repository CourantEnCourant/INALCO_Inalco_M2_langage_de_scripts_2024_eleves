from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from datetime import datetime
import logging

from pathlib import Path
from typing import List, Tuple, Dict
import csv
from tqdm import tqdm

content2xpath = {
    'ID': '//*[@id="words-list"]/h3',
    'date': '//*[@id="text-details"]/div',
    'provenance': '//*[@id="text-details"]/p[1]/*[position()>1]',
    'material': '//*[@id="text-details"]/p[3]/*[position()>1]',
    'content': '//*[@id="text-details"]/p[5]',
    'publications': '//*[@id="text-publs"]/*[position()>1]',
    'collections': '//*[@id="text-coll"]/*[position()>1]',
    'archive': '//*[@id="text-arch"]/*[position()>1]',
    'full_text': '//*[@id="words-full-text"]/*'
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


def main(input_file: Path, output_file: Path, log_file: Path) -> None:
    # Configurate logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=log_file,
                        filemode='w')

    # Get urls from input file
    with open(input_file, "r") as f:
        urls = f.read().splitlines()
    logging.info(f"Got {len(urls)} urls")

    # Configurate driver
    driver = webdriver.Chrome(service=Service())
    driver.implicitly_wait(5)

    # Scrap pages
    pages = []
    for url in tqdm(urls, desc='Scrapping'):
        page = scrap_papyrus(url, driver)
        pages.append(page)

    # Output to .csv
    with open(output_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(pages[0].keys())
        for page in tqdm(pages, desc="Output to csv"):
            writer.writerow(page.values())
        logging.info(f"Output saved to {output_file}")


if __name__ == '__main__':
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', default='../data/urls.txt', type=Path, help="File containing url to scrap.")
    parser.add_argument('-o', '--output_file', default='../data/corpus_scrapped.csv', type=Path, help="Output .csv file.")
    parser.add_argument('-l', '--log_file', default=f'../logs/log_{current_time}.txt', type=Path, help="Log file.")
    args = parser.parse_args()

    main(input_file=args.input_file,
         output_file=args.output_file,
         log_file=args.log_file)
