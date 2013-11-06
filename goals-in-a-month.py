import query_profiler as qp

attempts = [
{"query": '''MATCH (player:Player)-[:scored_in]->game<-[:in_month]-month, player-[:played]->stats-[:in]->game
			 WHERE player.name = "Michu"
			 WITH DISTINCT month, stats
          	 WITH month, SUM(stats.goals) AS totalGoals
			 ORDER BY month.position
			 RETURN month.name, totalGoals'''},

{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game
			 WHERE player.name = "Michu"
			 WITH player, stats, game
			 MATCH (player)-[:scored_in]->(game)<-[:in_month]-(month)
			 WITH DISTINCT stats, month
			 WITH month, SUM(stats.goals) AS totalGoals
			 ORDER BY month.position
			 RETURN month.name, totalGoals'''},

{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game
			 WHERE player.name = "Michu"
			 WITH player, stats, game
			 MATCH (player)-[:scored_in]->(game)<-[:in_month]-(month)
			 WITH month, COLLECT(DISTINCT stats) AS allTheGames
			 ORDER BY month.position
			 RETURN month.name, REDUCE(total = 0, g in allTheGames | total + g.goals) AS totalGoals'''},

{"query": '''MATCH (player:Player)-[:scored_in]->game
			 WHERE player.name = "Michu"
			 WITH DISTINCT player, game
			 MATCH game<-[:in_month]-month, player-[:played]->stats-[:in]->game
          	 WITH month, SUM(stats.goals) AS totalGoals
			 ORDER BY month.position
			 RETURN month.name, totalGoals'''},			 
]

qp.profile(attempts, iterations=100, runs=3)