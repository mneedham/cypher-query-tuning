### Tuning them cypher queries

Install the following python libraries:

    pip install py2neo numpy

I'm using version 1.6 on py2neo so get that version if you can.

You'll also need to replace the following function in 'util.py' in order that UTF-8 characters get handled correctly:

    ````python
    def is_collection(obj):
        """ Returns true for any iterable which is not a string or byte sequence.
        """
        if isinstance(obj, bytes):
            return False
        try:
            iter(obj)
        except TypeError:
            return False
        try:
            if type(obj) is list:
                hasattr(None, obj)
            else:
                hasattr(None, obj.encode("utf-8"))
        except TypeError:
            return True
        return False
    ````    

The data set is on dropbox and you can download it with this command:

    curl -L https://www.dropbox.com/s/y4gp00gfryc9syx/football.zip -o football.zip

The zip contains the 'data' directory so you can unpack that into your neo4j folder:

	unzip football.zip -d /path/to/neo4j/

You can then run an example query which has been tuned:

    python top-away-scorers.py
    
    <snip>

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

#### Creating a new benchmark

This is the template to follow:

    import query_profiler as qp

    attempts = [
    {"query": '''MATCH (p:Player) RETURN COUNT(p)''', "params": {"define": "if you want"}},
    {"query": '''MATCH (player:Player) RETURN COUNT(player)'''},
    ]

    qp.profile(attempts, iterations=5, runs=3)