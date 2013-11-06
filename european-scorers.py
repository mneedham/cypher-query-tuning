import query_profiler as qp

# This one becomes quicker towards the end by reducing the number of paths that we apply 'ORDER BY goals' on 
# Instead we use a WHERE earlier in the query to remove some paths

attempts = [
{"query": '''MATCH (continent:Continent)<-[:is_in]-(country:Country)<-[:comes_from]-(player:Player)
             WHERE continent.name = "Europe" 
             WITH player, country
             MATCH (player)-[:played]->(stats)-[:for]->(team:Team)
             RETURN player.name, SUM(stats.goals) AS goals, team.name, country.name
             ORDER BY goals DESC
             LIMIT 10'''},

{"query": '''MATCH (continent:Continent)<-[:is_in]-(country)<-[:comes_from]-(player)
			 WHERE continent.name = "Europe" 
     		 WITH player, country
			 MATCH (player)-[:played]->(stats)-[:for]->(team:Team)
			 RETURN player.name, SUM(stats.goals) AS goals, team.name, country.name
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (continent:Continent)<-[:is_in]-(country)
			 WHERE continent.name = "Europe" 
     		 WITH country
     		 MATCH (country)<-[:comes_from]-(player)
     		 WITH player, country
			 MATCH (player)-[:played]->(stats)-[:for]->(team:Team)
			 RETURN player.name, SUM(stats.goals) AS goals, team.name, country.name
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (continent:Continent)<-[:is_in]-(country)
			 WHERE continent.name = "Europe" 
     		 WITH country
     		 MATCH (country)<-[:comes_from]-(player)
     		 WITH player, country
			 MATCH (player)-[:played]->(stats)-[:for]->(team:Team)
			 WHERE stats.goals > 0
			 RETURN player.name, SUM(stats.goals) AS goals, team.name, country.name
			 ORDER BY goals DESC
			 LIMIT 10'''},

{"query": '''MATCH (continent:Continent)<-[:is_in]-(country)
			 WHERE continent.name = "Europe" 
     		 WITH country
     		 MATCH (country)<-[:comes_from]-(player)
     		 WITH player, country
			 MATCH (player)-[:played]->(stats)-[:for]->(team)
			 WHERE stats.goals > 0
			 RETURN player.name, SUM(stats.goals) AS goals, team.name, country.name
			 ORDER BY goals DESC
			 LIMIT 10'''},				 
]

qp.profile(attempts, iterations=20, runs=3)