def lookup(index, keyword):
    if keyword in index:
		return index[keyword]
    return None
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
					newrank = newrank + d * (ranks[node] / len(graph[node]))
			newranks[page] = newrank
		ranks = newranks
	return ranks
def multi_lookup(index, query):
    seen = {}
    result = []
    for word in query:
        if word in index:
            for i in index[word]:
                if i[0] in seen:
                    seen[i[0]].append(i[1])
                else:
                    seen[i[0]] = [i[1]]  
    if len(query) > 1:
        for url in seen:
            check = True
            for k in range(0,len(seen[url])-1):
                if (seen[url][k] +1) != (seen[url][k+1]):
                    check = False
            if check:
                result.append(url)        
    else :
        for url in seen:
            result.append(url)
    if len(result) == 0:
        return None
    return result
def lucky_search(index, ranks, keywords):
	result = lookup(index,keywords)
	if not result:
		return None
	best=result[0]
	for i in result:
		if ranks[i] > best:
			best = ranks[i]
	return best
def quicksort(pages, ranks):
	if not pages or len(pages) <= 1:
		return pages
	else:
		pivot = ranks[pages[0]]
		worse = []
		better = []
		for page in pages[1:]:
			if ranks[page] <=pivot:
				worse.append(page)
			else:
				better.append(page)
		return quicksort(better,ranks) + [pages[0]] + quicksort(worse,ranks)
def search(index, ranks, keyword):
	pages = lookup(index,keyword)
	return quicksort(pages,ranks)