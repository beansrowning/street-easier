import argparse
from service.db import StreetEasyDataBase
import service.web as web

def main(args):
    # Initiate data store
    # datastore = StreetEasyDataBase()

    # Run in headless mode, assuming we passed a query already
    if args.query is not None:
        se_search_query = arg.query
        se_full_url = "https://streeteasy.com/for-rent/{}".format(se_search_query)
    else:
        # Run interactive, wait for input before proceeding with the scraping.
        se_full_url = "https://www.streeteasy.com"
    
    se_session = web.ResultPages(url = se_full_url)

    if not args.headless:
        _ = input("Running scraper interactive. Search query in browser and press any key to continue.")

    

    # Pull all URLs for every listing
    se_session.get_all_listings()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--interactive",
        help="Run in interactive mode, selecting search terms manually on page before scrape",
        dest="headless",
        action="store_false"
        )
    parser.set_defaults(headless = True)
    parser.add_argument("--query",
                    type=str,
                    help="A street easy query to scrape from (i.e. url after streeteasy.com/for-rent/...)")

    arg = parser.parse_args()
    main(arg)