import timeit
import re
import numpy as np

def profile(attempts, iterations=10, runs=3):	
	for attempt in attempts:
		global a 
		a = attempt
		setup = '''
from query_profiler import a
import neo4j
'''
		timings = timeit.repeat("neo4j.Neo4j().query(a)", setup=setup, number=iterations, repeat=runs)
		print ""		
		print re.sub('\n[ \t]', '\n', re.sub('[ \t]+', ' ', attempt['query']))
		print "Min", np.min(timings), "Mean", np.mean(timings), "95%", np.percentile(timings, 95), "Max", np.max(timings)
		print ""