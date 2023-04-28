import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from service.db import StreetEasyDataBase
import service.web as web

def main():
    datastore = StreetEasyDataBase()

    # while True:
    #     links = scraper.get_link_by_class("mw-jump-link")
    #     for link in links:
    #         print(link.get_attribute('href'))

    #     scraper.next_page()

    #     if not scraper.next_page_button:
    #         break

if __name__ == "__main__":
    main()