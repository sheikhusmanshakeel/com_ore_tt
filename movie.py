#!/bin/python3

import os

import requests

# Complete the function below.
template_url = "http://jsonmock.hackerrank.com/api/movies/search/?Title={0}"
template_url_with_pageNumber = "http://jsonmock.hackerrank.com/api/movies/search/?Title={0}&page={1}"


def getMovieTitles(substr):
    f = open(os.environ['OUTPUT_PATH'], 'w')
    try:
        _substr = str(input())
    except:
        _substr = None

    res = get_titles_list(_substr)
    for res_cur in res:
        f.write(str(res_cur) + "\n")
    f.close()


def parse_data(data):
    title_array = []
    for row in data:
        if row["Title"]:
            title_array.append(row["Title"])
    return title_array


def get_response(url):
    response = None
    try:
        r = requests.get(url=url.format(url))
        if r and r.status_code == 200:
            response = r.json()
            if not response["data"] or len(response["data"]) == 0:
                # If no data is returned, then treat the request as returning null
                response = None
    except:
        print("Error while parsing URL: {0}".format(url))
    return response


def get_titles_list(movie_title):
    titles = []
    response = get_response(template_url.format(movie_title))

    if response:
        total_pages = response["total_pages"]
        total_results = response["total"]
        titles = [""] * total_results
        titles += parse_data(response["data"])
        if total_pages > 1:
            for i in range(2, total_pages + 1):
                response = get_response(template_url_with_pageNumber.format(movie_title, i))
                if response:
                    titles += parse_data(response["data"])
                else:
                    print("No data returned from page: {0}".format(i))
    else:
        print("No response returned for movie: {0}".format(movie_title))
    return titles


if __name__ == "__main__":
    titles = get_titles_list("spiderman")
    titles = sorted(titles, key=str.lower)
    print(titles)
    print(len(titles))