import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

LINE_TOKEN = os.getenv("LINE_TOKEN")

def lineNotifyMessage(msg):
    headers = {
        "Authorization": "Bearer " + LINE_TOKEN, 
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
    lineNotifyMessage(message)
    return message

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour='*')
    scheduler.start()
