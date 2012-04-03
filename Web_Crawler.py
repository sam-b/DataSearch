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
	index = {}
	graph = {}
    depth = 0
	pages = 0
    while tocrawl and pages < max_pages:
        page = tocrawl.pop()
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
	
def add_page_to_index(index, url, content):
	split_list = " ,!-"
    words = split_string(content,split_list);
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
        if keyword in index:
            index[keyword].append(url)
        else:
			index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
		return index[keyword]
    return None
	
def split_string(source,splitlist):
    string = "";
    out = [];
    while True:
        if source=="":
            return out;
        if source[0] not in splitlist:
            string = string + source[0];
        if source[0] in splitlist:
            out.append(string);
            string = "";
        source = source[1:];
		
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
                for node in graph:
                    if page in graph[node]:
                        newrand = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks
	
def lucky_search(index, ranks, keyword):
    best = 0
    out = ""
    if keyword not in index:
        return None
    for i in index[keyword]:
        if ranks[i] > best:
            best = ranks[i]
            out = i
    return out
	
index, graph = crawl_web("http://www.engimagroup.org",10,100)
ranks = compute_ranks(graph)
print lucky_search(index,ranks,"hello")