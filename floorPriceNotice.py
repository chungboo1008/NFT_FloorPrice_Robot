import os
import requests
import discord
from discord.ext import tasks
from discord.ext import commands

client = commands.Bot(command_prefix="!")
LINE_TOKEN = os.getenv("LINE_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL = os.getenv("CHANNEL")

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    r = requests.post(
        "https://notify-api.line.me/api/notify",
        headers = headers,
        params = payload
    )
    return r.status_code

def msgFormat(project, floor_price):
    msg = ''
    for i in range(len(project)):
        str = f'{project[i]}: {floor_price[i]}'
        msg += str
        msg += '\n'
    return msg
    
def job():
    token = 'LINE_TOKEN'

    project_list = [
        'Meebits',
        'ALPACADABRAZ',
        'ALPACADABRAZ 3D',
        'Zoofrenz',
        'Cupcat Kittens'
    ]
    url_list = [
        'https://api.opensea.io/collection/meebits',
        'https://api.opensea.io/collection/alpacadabraz',
        'https://api.opensea.io/collection/alpacadabraz-3d',
        'https://api.opensea.io/collection/zoofrenznft',
        'https://api.opensea.io/collection/cupcatkittens'
    ]

    response = []
    floor_price = []
    for index in range(len(url_list)):
        response = requests.request("GET", url_list[index])
        floor_price.append(response.json()['collection']['stats']['floor_price'])

    message = msgFormat(project_list, floor_price)
    lineNotifyMessage(token, message)
    return message

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(hours=1) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(CHANNEL) # channel ID goes here
        msg = job()
        await channel.send(msg)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

if __name__ == '__main__':
    client = MyClient()
    client.run(DISCORD_TOKEN)
