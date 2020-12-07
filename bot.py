import discord
from requests import get
import csv
import mcipc
import traceback

whitelist_filename = 'whitelist.csv'
ip = get('https://api.ipify.org').text

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

file = open('rcon.txt', 'r')
rcon_password = file.read().strip()
file.close()

def get_players() -> str:
    try:
        with mcipc.rcon.Client('127.0.0.1', 25575) as client:            
            client.login(rcon_password)
            
            player_info = client.players
            if player_info[0] == 0:
                return "no one online"
            else:
                result = f'There are {player_info[0]} of a max of {player_info[1]} players online:\n'
                return result +"".join(str(player)+"\n" for player in player_info[2])
    except OSError or ConnectionError:
        return "server offline or otherwise unable to connect :("

def send_command(command) -> str:
    with mcipc.rcon.Client('127.0.0.1', 25575) as client:            
        client.login(rcon_password)
        return client.run(command)

class Whitelist():
    def __init__(self):
        self._users_dict = dict()
        with open(whitelist_filename, mode='r') as csv_file:
            for row in csv.reader(csv_file, delimiter=','):
                self._users_dict[row[0]] = row[1]        
    
    def _write_file(self):
        with open(whitelist_filename, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for discord, minecraft in self._users_dict.items():
                csv_writer.writerow([discord, minecraft])
                    
    def get_users(self) -> str:
        users_str = 'all users in whitelist:\n'
        for discord, minecraft in self._users_dict.items():
            users_str += f'{discord} -> {minecraft}\n'
        users_str += f'{len(self._users_dict)} users'
        
        return users_str
        
    def add_user(self, discord, minecraft) -> str:
        old_username = ''      
        if discord in self._users_dict:
            old_username = self._users_dict[discord]
            
        send_command(f'whitelist remove {old_username}')
        send_command(f'whitelist add {minecraft}')
        
        self._users_dict[discord] = minecraft
        self._write_file()
        return f'your minecraft username has been updated to {minecraft}'

class DiscordClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(619042012640837633)
        await channel.send(f'<@&775201643133403137> Server online at: {ip}')
        print(f'logged in as {self.user} and posted public IP')
 
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.author.id == 180531137330937856 and message.content.startswith('/rcon '):
            try:
                response = send_command(message.content[6:])
            except:
                response = traceback.format_exc()
            await message.channel.send(response)
            
        # DM only
        if message.channel.type == discord.ChannelType.private:
            if message.content.startswith('/nocontext '):
                channel = client.get_channel(619729375192940553)
                await channel.send(message.content[11:])
         
        # DM or bot-commands channel
        if message.channel.type == discord.ChannelType.private \
           or message.channel.id == 619042012640837633:
            if message.content == '/help':
                await message.channel.send('all commands:\n' +
                                           '/status -> shows ip of server\n' +
                                           '/whomst -> lists players online\n' +
                                           '/whitelist -> view players on whitelist\n' +
                                           '/whitelist "minecraft username" -> add username to server whitelist (no quotes around username)\n' +
                                           '/nocontext "quote" -> anonymously post a quote to out-of-context-quotes (must DM bot)')
                 
            if message.content == '/status':
                await message.channel.send(f'server online at: {ip}\n' +
                                           "don't forget to add yourself to the whitelist! (/help)")
                 
            if message.content == '/whomst' or message.content == '/list':
                try:
                    response = get_players()
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
             
            if message.content == '/whitelist':
                try:
                    response = Whitelist().get_users()
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
             
            if message.content.startswith('/whitelist '):
                try:
                    response = Whitelist().add_user(str(message.author), message.content[11:])
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
                
            if message.content == '/poweroff':
                await message.channel.send('power off feature coming soon')
 
            if message.content == '/nocontext':
                await message.channel.send('random out of context quote feature coming soon')

if __name__ == "__main__":
    client = DiscordClient()
    client.run(token)
    