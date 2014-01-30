python-web-crawler-guide
========================

Project guide for a python web crawler project.  Made for the Python stride on 01/29/14.

## How to use this guide
As Zed Shaw states on his site programming-motherfucker.com, the best way to learn programming is to, well, "Program, motherfucker."  Don't just copy and paste the code from this guide, or just settle for reading through and "understanding" the code.  Understanding comes through doing, so open up that terminal and start writing.

## What is a Web Crawler?

From Wikipedia, "A web crawler is an Internet bot that systematically indexes the World Wide Web, typically for the purpose of Web indexing".  This basically means that you start with a page or set of web pages, find all the links in those pages, and get the pages from those links, and then the links on those pages... etc.  As you can see, this is an instrisically recursive process.

Google uses web crawlers to index the web, web crawlers that take into consideration the quality of the content, how many times a web page has already been "crawled" on, and much more.  Ours will obviously be much simpler.  This is just to show you after you get this working, there is still much more that can be done to enhance it.

## Alright, let's code

First, we need a way of making http requests to download web content.  `urllib2` is a python module we can use `httplib` is another.  For this project I used `urllib2` because of familarity. 

Next we also need a way of isolating the links in the web pages we need an html parser.  One is python library that is widely known is BeautifulSoup, but is a little slow for our purposes.  More preferable would be to use the `lxml.html` library.  So far you should have this:

```
imoprt urllib2    # Library for url fetching
import lxml.html  # Library for html parsing
```

If your python doesn't have lxml, download it via pip on the command line: `pip install lxml`

Now onto the crawler logic.  As I mentioned before, web crawling is a recursive process, but to have recursion we need to first define a function

```
def crawl(url, depth=3):  
```

where the function is named `crawl` it takes one or two arguments, with the depth being an optional argument and having a default value of 3.  The url is going to be the string url that we will start at and the depth indicates how many levels should be travelled before stopping.  Therefore the base case of recursion is when depth is 0.  Hence:

```
	if depth == 0:  # Recursion base case, return nothing
		return None
```

Now we come to the meat of the program.  We need to fetch the page, parse the content, extract the links, and crawl to those links.  Lets start with the web page fetching and parsing

```
	try:
		page = urllib2.urlopen(url)  # fetch the page
	except (urllib2.URLError, ValueError):
		 return None  # if there was an error, bail
		 
	html = page.read()  # read the html
	dom = lxml.html.fromstring(html) # parse the html
	
	print "Level %d: %s" % (depth, url)
```

I know there's a lot going on here. This might be your first time seeing a try/except block in python.  The basic idea is everything in the try block is 'tried' to run.  If the code in the `try` block throws an exception, then code execution instantly jumps to the `except` line, where it checks if the exception thrown matches one of those in the n-tuple.  If it does, then the `except` block gets run.  We want to make sure if we get some ill-formatted url's, or fail to make a connection to the remote server, our code doesn't stop, instead it just returns nothing. 

The next two lines are fairly straight forward.  `urllib2.urlopen` returns essentially a special file, so we read that file and store the string in a variable called `html`.  We then use the html parser `lxml.html` to get the parser object, and we call it `dom` for [Document Object Model](http://en.wikipedia.org/wiki/Document_Object_Model). 

We can use this parser object to extract the links.  Like so:

```
	for link in dom.xpath('//a/@href'):
		crawl(link, depth - 1)
```

`dom.xpath('//a/@href')` finds all the anchor tags and pells the hrefs from them.  We iterate on those links and crawl on each of them.  We subtract 1 from the depth since we are entering a new level.  

With this you should have a working web crawler, that will print out the links travelled, and which level those links are at.

```
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
```


## What's Next