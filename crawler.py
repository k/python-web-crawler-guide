import urllib2
from BeautifulSoup import BeautifulSoup

startingURL = "http://ieee.rutgers.edu"


def crawl(url, prevLevel=0):
    if prevLevel > 1:
        return None
    try:
        page = urllib2.urlopen(url)
    except (urllib2.URLError, ValueError):
        return None

    try:
        soup = BeautifulSoup(page)
    except UnicodeEncodeError:
        return None
    root = {}
    root["url"] = url
    root["children"] = []

    anchors = soup.findAll('a')
    for a in anchors:
        link = a.get('href')
        if link is not None:
            child = crawl(a['href'], prevLevel + 1)
            if child is not None:
                print child["url"]
                root["children"].append(child)

    root["content"] = soup.renderContents()
    return root

crawl(startingURL)
