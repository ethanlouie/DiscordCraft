from mcipc.query import Client

def get_players(host,port):
    try:
        with Client(host, port) as client:
            players = client.full_stats.players
            if len(players) == 0:
                return "no one online"
            elif len(players) > 0:
                result = "Who's online:\n"
                return result +"".join(str(player)+"\n" for player in players)
    except ConnectionError:
        return "server offline or otherwise unable to connect :("

#test it out wit dis
print(get_players("68.109.198.55",25565))