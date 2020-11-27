from mcipc.query import Client

def get_players(host,port):
    try:
        with Client(host, port) as client:
            players = client.full_stats.players
            if len(players) == 0:
                return "no one online"
            elif len(players) > 0:
                return "players online:".join(str(player)+"\n" for player in players)
    except ConnectionError:
        return "server offline or otherwise unable to connect :("


