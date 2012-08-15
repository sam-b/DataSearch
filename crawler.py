import urllib
#gets page contents
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""
def add_page_to_index(index, url, content):
	split_list = " ,!-"
	words = split_string(content,split_list);
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
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
def split_string(source,splitlist):
    out = [];
    atsplit = True
    for char in source:
    	if char in splitlist:
    		atsplit = True
    	else:
    		if atsplit:
    			out.append(char)
    			atsplit = False
    		else:
    			out[-1] = out[-1] + char
    return out
def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]
def crawl_web(seed,max_depth,max_pages):
	tocrawl = [seed]
	crawled = []
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
				add_page_to_index(index, page, content)
				links = get_all_links(content)
				graph[page]=links
		                union(tocrawl, links)
		                depth = depth + 1
	        crawled.append(page)
		pages = pages + 1
    	return index, graph 
