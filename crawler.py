import urllib
#gets page contents
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def add_page_to_index(index, url, content):
	words = content.split(" ,!-")
	for word in words:
	        add_to_index(index, word, url)

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

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]
def remove_tags(s):
	while True:
		start = s.find('<')
		if start == -1:
			return s.split()
		end = s.find('>')
		s = s[:start] + ' ' + s[end + 1:]
def crawl_web(seed,max_depth,max_pages):
	tocrawl = set([seed])
	crawled = set()
	index = {}
	graph = {}
	depth = 0
	pages = 0
	while tocrawl and pages < max_pages:
		page = tocrawl.pop()
		print page
		if page not in crawled:
			if depth <max_depth:
				content = get_page(page)
				words = remove_tags(content)
				add_page_to_index(index, page, words)
				links = get_all_links(content)
				graph[page]=links
		                tocrawl.update(links)
		                depth = depth + 1
	        crawled.add(page)
		pages = pages + 1
    	return index, graph 
