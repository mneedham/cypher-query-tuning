import timeit

def profile(attempts, iterations=10, runs=3):	
	for attempt in attempts:
		global a 
		a = attempt
		setup = '''
from query_profiler import a
import neo4j
'''
		timings = timeit.repeat("neo4j.Neo4j().query(a)", setup=setup, number=iterations, repeat=runs)