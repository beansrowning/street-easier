from seleniumbase import Driver
from seleniumbase.fixtures.page_actions import hover_and_click, hover_on_element
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import random
import threading
import queue

class EasyCrawler():
    """
    A web crawler that handles the user session, pagination, and search
    """
    url = ""
    listings = list()

    def __init__(self, url = "https://streeteasy.com/for-rent/nyc/price:-4000%7Carea:301,302,117,109,402"):
        """
        Initialize the web driver and 
        """
        self.url = url
    
    def rand_wait_and_scroll(self, time_range: tuple[float, float] = (1.5, 5.), scroll_range: tuple[int, int] = (50, 200)):
        """
        Bot-detection defeat by random waiting and scrolling
        """
        to_wait = random.uniform(*time_range)
        to_scroll = random.uniform(*scroll_range)

        driver = self.driver
        WebDriverWait(driver, to_wait)
        driver.execute_script("window.scrollTo({}, {})".format(to_scroll, to_scroll)) 
    
    def hover_and_click_by_xpath(self, sel : str, wait : int = 5) -> None:
        """
        Short-hand to hover and click element based on XPath.
        By default, waits 5s to determine if element is clickable
        """
        driver = self.driver

        WebDriverWait(driver, wait).until(ec.element_to_be_clickable((By.XPATH, sel)))

        hover_and_click(
            driver,
            hover_selector = sel,
            click_selector = sel,
            hover_by = By.XPATH,
            click_by = By.XPATH
        )

    def navigate_in_new_page(self, url: str) :
        """
        Using pre-initialized driver, navigate to url in a new page
        and switch driver to new window.
        """
        driver = self.driver
        # BUG: driver.get doesn't work for some reason. Using this instead.
        self.driver.execute_script("window.open('{}')".format(url))
        # Swap DOM to open window

        driver.switch_to.window(driver.window_handles[1])

    def page_loaded(self, trigger_elem : str, timeout: int, by = By.CLASS_NAME) -> None:
        """
        Quick short-hand to detect if page is loaded
        by checking for the presence of an element
        """
        try:
            element_present = ec.presence_of_element_located((by, trigger_elem))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out after {}s waiting for page to load.".format(timeout))
        
        return None

    def __enter__(self, **kwargs):
        self.driver = Driver(uc=True)

        self.navigate_in_new_page(self.url)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Quit driver on exit from context manager
        """
        self.driver.quit()


class FirstPageSearch(EasyCrawler):
    """
    Currently a debugging class to try navigating the top-page serach function
    to avoid detection by passing straight search URL
    """
    # XPATH values for elements on the main page 
    top_page_elements = {
        "search_bar": '//div[contains(@class, "styled__LocationFilterWrapper")]//button',
        "search_bar_drilldown": '//button[text()="See all neighborhoods"]',
        "borough" : '//div[p[contains(text(), "{}")]]',
        "neighborhood" : '//div[p[contains(@class, "Text-sc-zyowvr-0 styled__NeighborhoodTitle") and contains(text(), "{}")]][1]//span',
        "search_apply" : '//button[text()="Apply"]',
        "min_price" : '//input[contains(@class, "TextField-minPrice")]',
        "max_price" : '//input[contains(@name, "max")]',
        "no_fee" : '//input[contains(@name, "no-fee")]',
        "search" : '//button[span[text()="Search"]]'
    }

    def test_entry(self):
        
        # Check that page is loaded based on first element we need to click
        self.page_loaded(self.top_page_elements["search_bar"], 10, by = By.XPATH)
        
        # Choose neighborhood and borough menu
        self.rand_wait_and_scroll()
        self.hover_and_click_by_xpath(self.top_page_elements["search_bar"])

        self.rand_wait_and_scroll()
        # Expand through to bring up all options
        self.hover_and_click_by_xpath(self.top_page_elements["search_bar_drilldown"])

        self.rand_wait_and_scroll()
        # Choose borough
        self.hover_and_click_by_xpath(self.top_page_elements["borough"].format("Manhattan"))

        self.rand_wait_and_scroll()

        # Choose neighborhood
        self.hover_and_click_by_xpath(self.top_page_elements["neighborhood"].format("Chelsea"))

        self.rand_wait_and_scroll()

        # Apply changes
        self.hover_and_click_by_xpath(self.top_page_elements["search_apply"])


        self.rand_wait_and_scroll()

        # Search
        self.hover_and_click_by_xpath(self.top_page_elements["search"])
        input("Check and see if it worked")


class ResultPages(EasyCrawler):
    """
    The result page of the streeteasy web search that contains potential listings
    that match our results
    """
    listing_a_class = "listingCard-globalLink jsGlobalListingCardLink"

    def get_all_listings(self):
        """
        Retrieve all listing URLs across all pages
        """
        page_status_code = 0
        page = 1


        while page_status_code == 0:
            print("Retrieving all listings, page {}".format(page))

            # Pull all listings on the current page
            self.get_listings()

            # Try to navigate to next page
            # or return 1 and break loop if
            # end of results
            page_status_code = self.next_page()

            page += 1
        
        print("All listings identified.")


    def next_page(self) -> int:
        """
        Navigate to the next page of results
        """
        driver = self.driver

        try:
            next_page_button = driver.find_element(By.XPATH, "//a[@rel='next']")
        except:
            return 1
        
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)

        self.hover_and_click_by_xpath("//li[@class='next']")

        return 0

    def get_listings(self, timeout = 20):
        driver = self.driver

        # Block waiting for page load
        self.page_loaded("searchCardList--listItem", timeout)

        # DEBUG
        input("press enter to continue.")

        # Save page soup
        self.page_soup = BeautifulSoup(driver.page_source, features="lxml")

        listing_cards = self.page_soup.find_all('li', {'class': 'searchCardList--listItem'})

        self.listings.append([listing_cards])
        # Extract attributes from listings pages
        for listing in listing_cards:
            top_level_attr = dict()

            pass

            # TODO: Extract all listing details from page,
            # then init new ListingPage class and extract those details
            # from downstream methods
            # self.listings.append(
            #     ListingPage(url=link.get_attribute('href'))
            # )

class ListingPage(EasyCrawler):
    """
    An apartment listing page that we've identified from a list of results from ResultPage
    """
    listing_details = {
        "neighborhood": None,
        "address": None, 
        "rooms": None,
        "price": None,
        "days_on_market": None,
        "geo": None,
        "beds": None, 
        "baths": None, 
        "sqft": None,
        "url": None
    }

    def __init__(self, url: str):
        super().__init__(url=url)

        # snapshot page source and use BS4 to parse
        self.source =  self.driver.page_source
        self.soup = BeautifulSoup(self.source)

    def parse_listing(self):
        pass

        # When Available
        # -> //div[h6[contains(text(), "Available on")]]//div[contains(@class, "Vitals-data")] text
        # Days on Market
        # -> //div[h6[contains(text(), "Days On Market")]]//div[contains(@class, "Vitals-data")] text
        # Price Change
        # -> //div[h6[contains(text(), "Last Price Change")]]//div[contains(@class, "Vitals-data")] text
        # Saves
        # -> //div[contains(@class, "popularity")] text
        # Main Amenities
        # -> //ul[contains(@class, "AmenitiesBlock")]//li
        # Bldg Amenities
        # -> //ul[contains(@class, "AmenitiesBlock-list")]//li
        # Borough, neighborhood hierarchy (multiple items, subtract the first which is "rentals")
        # //ul[contains(@class, "Breadcrumb Breadcrumb--detailsPage")]//span[contains(@itemprop, "name")]