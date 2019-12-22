import requests
import logging

# set up the logger
logger = logging.getLogger('movie_parser')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MovieWebScraper:
    """
    Class to get data from hackerrank website using their movies api
    """
    def __init__(self, movie_title):
        self.movie_name = movie_title
        self.url = "http://jsonmock.hackerrank.com/api/movies/search/?Title={0}"
        self.url_with_pageNumber = "http://jsonmock.hackerrank.com/api/movies/search/?Title={0}&page={1}"
        self.titles = []
        self.total_pages = 0
        self.current_index = 0

    def parse_data(self, data):
        """
        Parse data to get the Title and fill up the movie title list
        :param data:
        :return:
        """
        for row in data:
            if row["Title"]:
                self.titles[self.current_index] = (row["Title"])
                self.current_index += 1

    def get_response(self, url):
        """
        Make HTTP Get request and return the response if not empty, otherwise return None
        :param url:
        :return:
        """
        response = None
        try:
            r = requests.get(url)
            if r and r.status_code == 200:
                response = r.json()
                if not response["data"] or len(response["data"]) == 0:
                    # If no data is returned, then treat the request as returning null
                    response = None
        except:
            logger.critical("Error while parsing URL: {0}".format(url), exc_info=True)
        return response

    def get_titles(self):
        """
        Generates the movie titles array
        :return:
        """
        response = self.get_response(self.url.format(self.movie_name))
        if response:
            total_pages = response["total_pages"]
            total_results = response["total"]
            self.titles = [""] * total_results
            self.parse_data(response["data"])
            if total_pages > 1:
                for i in range(2, total_pages + 1):
                    response = self.get_response(self.url_with_pageNumber.format(self.movie_name, i))
                    if response:
                        self.parse_data(response["data"])
                    else:
                        logger.error("No data returned from page: {0}".format(i))
        else:
            logger.critical("No response returned for movie: {0}".format(self.movie_name))

    def process_movie_request(self):
        """
        Main class function which generates and prints a sorted movie list
        :return:
        """
        self.get_titles()
        titles = sorted(self.titles, key=str.lower)
        logger.info(titles)
        logger.info("Total titles returned: {0}".format(len(titles)))


if __name__ == "__main__":
    movie = "douchebag"
    m = MovieWebScraper(movie)
    m.process_movie_request()
