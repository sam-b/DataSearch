import urllib
#gets page contents
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""
#finds the next link
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
#for each item in list q appends it to list p if it is not already in list p
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

#gets all the links in a page
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links
#crawls the web
def crawl_web(seed,max_depth,max_pages):
    tocrawl = [seed]
    crawled = []
    depth = 0
	pages = 0
    while tocrawl and pages < max_pages:
        page = tocrawl.pop()
        if page not in crawled:
            if depth <max_depth:
                union(tocrawl, get_all_links(get_page(page)))
                depth = depth + 1
            crawled.append(page)
			pages = pages + 1
    return crawled 