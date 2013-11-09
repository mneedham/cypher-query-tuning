from py2neo import neo4j

class Neo4j:
	def __init__(self):
		self.graph_db = neo4j.GraphDatabaseService()

	def query(self, attempt):
		query = attempt["query"]
		potential_params = attempt.get("params")		
		params = {} if potential_params == None else potential_params
		return self.run_query(query, params)

	def run_query(self, query, params):
		query = neo4j.CypherQuery(self.graph_db, query)
		return query.execute(**params).data