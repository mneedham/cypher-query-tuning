import query_profiler as qp

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
			 LIMIT 10'''}
]

qp.profile(attempts, iterations=5, runs=3)