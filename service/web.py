from seleniumbase import Driver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

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

        self.driver = Driver(uc=True)

        # Navigate to top-level
        self.driver.get(self.url)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Quit driver on exit from context manager
        """
        self.driver.quit()

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
            next_page_click = driver.find_element(By.XPATH, "//li[@class='next']")
            next_page_button = driver.find_element(By.XPATH, "//a[@rel='next']")
        except:
            return 1
        
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
        # next_page_click.click_safe()

        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(next_page_button))
        next_page_click.click()
        # driver.execute_script("arguments[0].click();", next_page_button)

        return 0

    def page_loaded(self, timeout) -> None:
        try:
            element_present = ec.presence_of_element_located((By.CLASS_NAME, 'searchCardList--listItem'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out after {}s waiting for page to load.".format(timeout))
        
        return None

    def get_listings(self, timeout = 20):
        driver = self.driver

        # Block waiting for page load
        self.page_loaded(timeout)

        # DEBUG
        input("press enter to continue.")

        # Save page soup
        self.page_soup = BeautifulSoup(self.driver.page_source, features="lxml")

        listing_cards = self.page_soup.find_all('li', {'class': 'searchCardList--listItem'})

        self.listings.append([listing_cards])
        # Extract attributes from listings pages
        for listing in listing_cards:
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

        # neighborhood
        # 