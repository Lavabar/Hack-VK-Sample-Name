from urllib.request import urlopen
from urllib.parse import quote_plus
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def findConcert(search):
    search = search.encode("utf-8").decode("utf-8")
    print(search)
    domen = "https://meloman.ru"
    search = quote_plus(search.strip())
    url = domen + "/search/?q=" + search + "&search_type=afisha"
    print(url)

    try:
        html = urlopen(url)
    except HTTPError as e:
        return "OpenError"

    try:
        bsObj = BeautifulSoup(html.read(), "lxml")
        searchResult = bsObj.find("div", class_="search-results-list-item-description")
        if searchResult == None:
            return "NoConcert"
        resUrl = domen + searchResult.find("a", class_="search-link-text")["href"]
        return resUrl
    except AttributeError as e:
        return "PageParsingError"
    except BaseException as e:
        print(e)
        return "AnotherErrorWithParsing"
