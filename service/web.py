from selenium import webdriver

class EasyCrawler():
    """
    A web crawler that handles the user session, pagination, and search
    """

    listing_a_class = "listingCard-globalLink jsGlobalListingCardLink"
    url = ""
    listings = []

    def __init__(self, url = "https://streeteasy.com/for-rent/greenpoint/price:-4000", user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"):
        """
        Initialize the web driver and 
        """
        self.url = url
        self.user_agent = user_agent
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)
        driver = webdriver.Firefox(profile)
        # Navigate to top-level
        driver.get(self.url)

    def next_page(self):
        """
        Navigate to the next page of results
        """
        driver = self.driver

        try:
            next_page_button = driver.find_element_by_xpath("//a[@rel='next']")
        except:
            return False

        next_page_button.click()

    def get_listings(self):
        driver = self.driver
        links = driver.find_elements_by_class_name(self.listing_a_class)
        for link in links:
            self.listings.append(link.get_attribute('href'))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Quit driver on exit from context manager
        """
        self.driver.quit()

class ResultPage():
    """
    The result page of the streeteasy web search that contains potential listings
    that match our results
    """
    pass

class ListingPage():
    """
    An apartment listing page that we've identified from a list of results from ResultPage
    """
    pass

class Scraper():
    """
    A page scraper that performs parsing operations on
    street easy listings
    """
    pass