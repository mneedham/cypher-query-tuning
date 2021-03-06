import query_profiler as qp

# I couldn't find out a way to make this one quicker

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

{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game
             WHERE player.name = "Michu" AND stats.goals > 0
             WITH player, game, stats
             MATCH game<-[:in_month]-month
             WITH month, SUM(stats.goals) AS totalGoals
             ORDER BY month.position
             RETURN month.name, totalGoals'''},	

{"query": '''MATCH (player:Player)-[:played]->stats-[:in]->game
             WHERE player.name = "Michu" AND stats.goals > 0
             WITH player, game, stats.goals AS goals
             MATCH game<-[:in_month]-month
             WITH month, SUM(goals) AS totalGoals
             ORDER BY month.position
             RETURN month.name, totalGoals'''},	
]

qp.profile(attempts, iterations=100, runs=3)