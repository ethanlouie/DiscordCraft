import discord
from requests import get
import csv
import mcipc
import traceback
from datetime import datetime, timedelta
from os import system

intents = discord.Intents.default()
intents.members = True

whitelist_filename = 'whitelist.csv'
ip = get('https://api.ipify.org').text

file = open('token.txt', 'r')
token = file.read().strip()
file.close()

file = open('rcon.txt', 'r')
rcon_password = file.read().strip()
file.close()

LATE_ATTENDANCE_CUTOFF_MINS = 5

def print_text(message):
    output = 'START TRANSMISSION\N\N' 
    f = open('temp.txt', mode=w)
    f.write(f'START TRANSMISSION\n\n{message}\n\nEND TRANSMISSION')
    f.close()
    
    system('lp temp.txt')

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
    
class Attendance():
    def __init__(self, channel, initial_list):
        self.channel = channel
        self.start_time = datetime.now()
        self.sign_in_values = initial_list
    
    def sign_in(self, username) -> str:
        if self.sign_in_values[username] != 'absent':
            return f'{username} {self.sign_in_values[username]}'
            
        if datetime.now() < self.start_time + timedelta(minutes=LATE_ATTENDANCE_CUTOFF_MINS):
            self.sign_in_values[username] = 'on time'
        else:
            self.sign_in_values[username] = 'late'
            
        return f'{username} {self.sign_in_values[username]}'
    
    def get_attendance(self) -> str:
        result = 'on time:\n'
        for user, status in self.sign_in_values.items():
            if status == 'on time':
                result += str(user) + '\n'
                
        result += '\nlate:\n'
        for user, status in self.sign_in_values.items():
            if status == 'late':
                result += str(user) + '\n'
                
        result += '\nabsent:\n'
        for user, status in self.sign_in_values.items():
            if status == 'absent':
                result += str(user) + '\n'
                
        return result
    
    def write_to_file(self):
        with open(str(self.start_time)+'.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for username, status in self.sign_in_values.items():
                csv_writer.writerow([username, status])

class DiscordClient(discord.Client):
    
    def __init__(self, intents):
        self.attendance = None
        super().__init__(intents=intents)
    
    async def on_ready(self):
        channel = client.get_channel(619042012640837633)
#         await channel.send(f'<@&775201643133403137> Server online at: {ip}')
        print(f'logged in as {self.user} and posted public IP')
 
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Ethan only
        if message.author.id == 180531137330937856:   
            if message.content.startswith('/rcon '):
                try:
                    response = send_command(message.content[6:])
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
            
            if message.content == '/attendance start':
                try:
                    initial_list = dict()
                    guild = self.get_guild(612510788711874573)
                    role = discord.utils.get(guild.roles, id=683502748347662412)
                    for member in message.channel.members:
                        if role not in member.roles:
                            initial_list[member] = 'absent'
                
                    self.attendance = Attendance(message.channel, initial_list)
                    response = f'@everyone meeting has started. type "here" (no quotes) in the next {LATE_ATTENDANCE_CUTOFF_MINS} minutes to be counted as on time.'
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
            
            if message.content == '/attendance stop':
                try:
                    self.attendance.write_to_file()
                    response = 'attendance ended.\n' + self.attendance.get_attendance()
                    self.attendance = None
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)

        # Attendance channel
        if self.attendance != None and message.channel == self.attendance.channel:
            if message.content == '/attendance':
                try:
                    response = self.attendance.get_attendance()
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
                
            if message.content == 'here':
                try:
                    response = self.attendance.sign_in(message.author)
                except:
                    response = traceback.format_exc()
                await message.channel.send(response)
                        
        # DM only
        if message.channel.type == discord.ChannelType.private:
            if message.content.startswith('/nocontext '):
                channel = client.get_channel(619729375192940553)
                await channel.send(message.content[11:])
                
            if message.content.startswith('/print '):
                try:
                    print_text(message.content[7:])
                except:
                    await message.channel.send(traceback.format_exc())
                         
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
                
            if message.content == '/here':
                await message.channel.send('attendance feature coming soon')

if __name__ == "__main__":
    client = DiscordClient(intents=intents)
    client.run(token)
    
   