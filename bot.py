import discord
from requests import get

ip = get('https://api.ipify.org').text

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

class MyClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(770213216449069067)
        await channel.send(f'My public IP address is: {ip}')
        print(f'Logged in as {self.user} and posted public IP')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

client = MyClient()
client.run(token)
