import discord
from requests import get

ip = get('https://api.ipify.org').text
print('My public IP address is: {}'.format(ip))

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

client = MyClient()
client.run(token)