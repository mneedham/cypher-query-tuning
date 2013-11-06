### Tuning them cypher queries

Install the following python libraries:

    pip install py2neo numpy

The data set is on dropbox and you can download it with this command:

    curl -L https://www.dropbox.com/s/y4gp00gfryc9syx/football.zip -o football.zip

The zip contains the 'data' directory so you can unpack that into your neo4j folder:

	unzip football.zip -d /path/to/neo4j/

You can then run an example query which has been tuned:

    $ python top-away-scorers.py
    
    MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
    WHERE game<-[:away_team]-team
    RETURN player.name, SUM(stats.goals) AS goals
    ORDER BY goals DESC
    LIMIT 10
    Min 1.67394113541 Mean 1.68005379041 95% 1.687089324 Max 1.68808412552

    MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
    WITH player, stats, team, game
    MATCH team-[:away_team]->game
    RETURN player.name, SUM(stats.goals) AS goals
    ORDER BY goals DESC
    LIMIT 10
    Min 1.29312396049 Mean 1.31829198201 95% 1.3343367815 Max 1.33520197868

    MATCH (game:Game)<-[:away_team]-(team)
    WITH game, team
    MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
    RETURN player.name, SUM(stats.goals) AS goals
    ORDER BY goals DESC
    LIMIT 10
    Min 0.615420103073 Mean 0.618293762207 95% 0.622805333138 Max 0.623574018478

    MATCH (game)<-[:away_team]-(team:Team)
    WITH game, team
    MATCH (player:Player)-[:played]->stats-[:in]->game, stats-[:for]->team
    RETURN player.name, SUM(stats.goals) AS goals
    ORDER BY goals DESC
    LIMIT 10
    Min 0.57263302803 Mean 0.585222005844 95% 0.597485733032 Max 0.598978042603