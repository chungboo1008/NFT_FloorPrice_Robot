import os
import requests
import discord
from discord.ext import tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def msgFormat(project, floor_price):
    msg = '\n'
    for i in range(len(project)):
        str = f'{project[i]}: {floor_price[i]}'
        msg += str
        msg += '\n'
    return msg
    
def job():
    token = 'OTQ0OTYyMzUzOTE5ODMyMDY0'

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
    return message

heplMsg = '''
!floor [project name / number] -> return its floor price
!project -> return all project and its number
'''

project_and_id = '''

'''

project2id = {
    'Meebits': 'meebits',
    'ALPACADABRAZ': 'alpacadabraz',
    'ALPACADABRAZ_3D': 'alpacadabraz-3d',
    'Zoofrenz': 'zoofrenznft',
    'Cupcat Kittens': 'cupcatkittens',
    '1': 'meebits',
    '2': 'alpacadabraz',
    '3': 'alpacadabraz-3d',
    '4': 'zoofrenznft',
    '5': 'cupcatkittens',
}

def search():
    message = 'haha'
    return message

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # start the task to run in the background
        # self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------------------------------------')
        

    async def on_message(self, message):
        #排除自己的訊息，避免陷入無限循環
        if message.author == client.user:
            return
        #如果以「說」開頭
        if message.content == '!floor' :
            msg = job()
            await message.channel.send(msg)
        elif message.content == 'help':
            await message.channel.send(heplMsg)
        
if __name__ == '__main__':
    client = MyClient()
    client.run(DISCORD_TOKEN)
