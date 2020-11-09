import discord
from requests import get

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
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.id == 619042012640837633:
            if message.content == '/status':
                await message.channel.send(f'Server online at: {ip}')

client = MyClient()
client.run(token)
