import urllib2
import lxml.html


def crawl(url, depth=3):
    if depth == 0:
        return None
    try:
        page = urllib2.urlopen(url)
    except (urllib2.URLError, ValueError):
        return None

    html = page.read()
    dom = lxml.html.fromstring(html)

    print "level %d: %s" % (depth, url)
    for link in dom.xpath('//a/@href'):
        crawl(link, depth - 1)
