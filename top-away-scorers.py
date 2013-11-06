from py2neo import neo4j
import timeit
import numpy as np
import re

graph_db = neo4j.GraphDatabaseService()

def run_query(query, params):
	query = neo4j.CypherQuery(graph_db, query)	
	return query.execute(**params).data

attempts = [
{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
			 WHERE game<-[:away_team]-team
			 RETURN player.name, SUM(stats.goals) AS goals
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
			 WITH player, stats, team, game
			 MATCH team-[:away_team]->game
			 RETURN player.name, SUM(stats.goals) AS goals
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (game:Game)<-[:away_team]-(team)
			 WITH game, team
			 MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
			 RETURN player.name, SUM(stats.goals) AS goals
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (game)<-[:away_team]-(team:Team)
			 WITH game, team
			 MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
			 RETURN player.name, SUM(stats.goals) AS goals
			 ORDER BY goals DESC
			 LIMIT 10'''},
]

print ""

for attempt in attempts:
	query = attempt["query"]
	potential_params = attempt.get("params")
	params = {} if potential_params == None else potential_params

	timings = timeit.repeat("run_query(query, params)", setup="from __main__ import run_query, query, params", number=10, repeat=3)

	print re.sub('\n[ \t]', '\n', re.sub('[ \t]+', ' ', query))
	print "Min", np.min(timings), "Mean", np.mean(timings), "95%", np.percentile(timings, 95), "Max", np.max(timings)
	print ""