from py2neo import neo4j
import timeit
import numpy as np
import re

graph_db = neo4j.GraphDatabaseService()

def run_query(query, params):
	query = neo4j.CypherQuery(graph_db, query)
	return query.execute(**params).data

def profile(attempts, iterations=10, runs=3):
	print ""

	for attempt in attempts:
		global _query
		_query = attempt["query"]
		potential_params = attempt.get("params")
		
		global _params
		_params = {} if potential_params == None else potential_params
	
		timings = timeit.repeat("run_query(_query, _params)", setup="from query_profiler import run_query; from query_profiler import _query, _params", number=iterations, repeat=runs)

		print re.sub('\n[ \t]', '\n', re.sub('[ \t]+', ' ', _query))
		print "Min", np.min(timings), "Mean", np.mean(timings), "95%", np.percentile(timings, 95), "Max", np.max(timings)
		print ""