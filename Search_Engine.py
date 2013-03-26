

import crawler
import RankAndSearch as core

if name == "__main__":
	print "Welcome to DataSearch!"
	print "Please enter a seed url!"
	seed = raw_input()
	print "Please enter a depth limit"
	depth = raw_input()
	print "Please enter a breadth limit"
	breadth = raw_input()
	index, graph = crawler.crawl_web(seed,depth,breadth)
	ranks = core.compute_ranks(graph)
	while True:
		print "please enter what you wish to search for!"
		term = raw_input()
		print core.search(index,ranks,term)
		print index
