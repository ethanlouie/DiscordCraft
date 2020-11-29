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
    except OSError or ConnectionError:
        return "server offline or otherwise unable to connect :("
    except Exception as e:
        return repr(e)
