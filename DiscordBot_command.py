import os
import csv
import requests
import discord
from discord.ext import tasks, commands

bot = commands.Bot(command_prefix='$')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
myChannel = 'command_line'

project2id = {}
with open('mapping_project2id.csv', newline='') as csvfile:
  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)
  for row in rows:
      project2id[row[0]] = row[1]

# for key in project2id.keys():
#     print(f'{key}: {project2id[key]}')

def getFloorPrice(project):
    projectId = project
    for p in project2id.keys():
        if project == p:
            projectId = project2id[project]
            break
    apiUrl = f'https://api.opensea.io/collection/{projectId}'
    response = requests.request('GET', apiUrl)


    message = f'Maybe \'{projectId}\' is wrong'
    if response.status_code == 200:
        floor_price = response.json()['collection']['stats']['floor_price']
        if floor_price == None:
            return message
    else:
        return message

    message = f'{projectId}: {floor_price}'
    return message

def getAllFloorPrice():
    temp = []
    message = ''
    for key in project2id.keys():
        if project2id[key] in temp:
            continue
        temp.append(project2id[key])
        apiUrl = f'https://api.opensea.io/collection/{project2id[key]}'
        response = requests.request("GET", apiUrl)
        if response.status_code != 200:
            continue
        floor_price = response.json()['collection']['stats']['floor_price']
        message += f'{project2id[key]}: {floor_price}\n'
    return message



@bot.command()
async def floor(message, arg):
    if str(message.channel) != myChannel:
        return
    project_name = arg
    msg = getFloorPrice(project_name)
    await message.channel.send(msg)

@bot.command()
async def floor_all(message):
    if str(message.channel) != myChannel:
        return
    msg = getAllFloorPrice()
    await message.channel.send(msg)

@bot.command()
async def insert(message, *args):
    project_name = args[0]
    project_id = args[1]
    for p_name in project2id.keys():
        if project_name == p_name:
            msg = f'Project name \'{project_name}\' is already exist!'
            await message.channel.send(msg)
            return
    with open('mapping_project2id.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([project_name, project_id])
    project2id[project_name] = project_id
    msg = f'Insert don!\nProject name: {project_name}\nProject id: {project_id}'
    await message.channel.send(msg)

@bot.command()
async def listDB(message):
    with open('mapping_project2id.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        msg = ''
        for row in rows:
            msg += f'{row[0]}: {row[1]}\n'
    await message.channel.send(msg)

@bot.command()
async def delete(message, arg):
    project_name = arg
    with open('mapping_project2id.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        dict = {}
        for row in rows:
            dict[row[0]] = row[1]

    dict.pop(project_name)
    with open('mapping_project2id.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['project name', 'url id'])
        for key in dict.keys():
            writer.writerow([key, dict[key]])
    msg = f'Delete Done.\n\'{project_name}\' is already remove.'
    await message.channel.send(msg)

# @bot.command()
async def help(message):
    if str(message.channel) != myChannel:
        return
    await message.channel.send("warning warning")
        
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
