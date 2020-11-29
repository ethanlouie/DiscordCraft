import discord
from requests import get
import server_stats

ip = get('https://api.ipify.org').text

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

class MyClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(619042012640837633)
        await channel.send(f'<@&775201643133403137> Server online at: {ip}')
        print(f'Logged in as {self.user} and posted public IP')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            if message.content.startswith('/nocontext '):
                channel = client.get_channel(619729375192940553)
                await channel.send(message.content[11:])

        if message.channel.type == discord.ChannelType.private \
           or message.channel.id == 619042012640837633:
            if message.content == '/help':
                await message.channel.send('help feature coming soon')
                
            if message.content == '/status':
                await message.channel.send(f'Server online at: {ip}')
                
            if message.content == '/whomst' or message.content == '/list':
                await message.channel.send(server_stats.get_players(ip,25565))

            if message.content == '/poweroff':
                await message.channel.send('power off feature coming soon')

            if message.content == '/nocontext':
                await message.channel.send('random out of context quote feature coming soon')

if __name__ == "__main__":
    client = MyClient()
    client.run(token)
