import discord
from requests import get
import server_stats
import csv
from mcipc.rcon import Client

whitelist_filename = 'whitelist.csv'
ip = get('https://api.ipify.org').text

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

file = open('password.txt', 'r')
rcon_password = file.read().strip()
file.close()

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
        try:            
            users_str = 'all users in whitelist:\n'
            for discord, minecraft in self._users_dict.items():
                users_str += f'{discord} -> {minecraft}\n'
            users_str += f'{len(self._users_dict)} users'
            
            return users_str
        except Exception as e:
            return repr(e)
        
    def add_user(self, discord, minecraft) -> str:
        try:            
            if discord in self._users_dict:
                pass
                #whitelist remove minecraft
            #whitelist add minecraft
            self._users_dict[discord] = minecraft
            self._write_file()
            return f'your minecraft username has been updated to {minecraft}'
        except Exception as e:
            return repr(e)
    
class MyClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(619042012640837633)
#        await channel.send(f'<@&775201643133403137> Server online at: {ip}')
        print(f'logged in as {self.user} and posted public IP')
 
    async def on_message(self, message):
        if message.author == self.user:
            return
         
        # DM only
        if message.channel.type == discord.ChannelType.private:
            if message.content.startswith('/nocontext '):
                channel = client.get_channel(619729375192940553)
                await channel.send(message.content[11:])
         
        # DM or bot-commands channel
        if message.channel.type == discord.ChannelType.private \
           or message.channel.id == 619042012640837633:
            if message.content == '/help':
                await message.channel.send('/status -> shows ip of server' +
                                           '/whomst -> lists players online' +
                                           '/whitelist -> view players on whitelist' +
                                           '/whitelist "minecraft username" -> add username to server whitelist (no quotes around username)')
                 
            if message.content == '/status':
                await message.channel.send(f'server online at: {ip}\n' +
                                           "don't forget to add yourself to the whitelist! (/help)")
                 
            if message.content == '/whomst' or message.content == '/list':
                await message.channel.send(server_stats.get_players(ip,25565))
             
            if message.content == '/whitelist':
                await message.channel.send(Whitelist().get_users())
             
            if message.content.startswith('/whitelist '):
                await message.channel.send(Whitelist().add_user(str(message.author), message.content[11:]))
 
            if message.content == '/poweroff':
                await message.channel.send('power off feature coming soon')
 
            if message.content == '/nocontext':
                await message.channel.send('random out of context quote feature coming soon')

if __name__ == "__main__":
    client = MyClient()
    client.run(token)

    with Client('68.109.198.55', 25565) as client:
        client.login(rcon_password)    # Perform initial login.
        print(client.seed)
        print(client.help())





