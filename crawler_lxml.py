import urllib2
import lxml.html
startingURL = "http://ieee.rutgers.edu"


def crawl(url, prevLevel=0):
    if prevLevel > 2:
        return None
    try:
        page = urllib2.urlopen(url)
    except (urllib2.URLError, ValueError):
        return None

    html = page.read()
    dom = lxml.html.fromstring(html)
    root = {}
    root["children"] = []
    root["url"] = url
    root["content"] = html

    for link in dom.xpath('//a/@href'):
        # Do anything to check link here
        child = crawl(link, prevLevel + 1)
        if child is not None:
            root["children"].append(child)

    return root

crawl(startingURL)
