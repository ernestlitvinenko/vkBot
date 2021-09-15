import vk_api
import os
import time
from datetime import datetime
from datetime import timedelta

# GRAB THIS TOKEN FROM https://oauth.vk.com/authorize?client_id=7951582&display=page&redirect_uri=http://vk.com/ernestlistvinenko&scope=groups,wall,photos,offline&response_type=token&v=5.65
TOKEN = "YOUR_TOKEN"

LOGIN = 'YOUR_VK_LOGIN'
PWD = 'YOUR_VK_PASSWORD'

# PUT YOUR PHOTOES TO ASSETS
PHOTO_FILEPATH = 'image.jpg'

# VK APPLICATION ID ( Don't touch it)
APP_ID = '7951582'

AT_TIME = '12:00'

def set_timer():
    hour, minute = map(int, AT_TIME.split(':'))
    current_date = datetime.today()
    
    query = {
        'days': 1,
        'hours': hour, 
        'minutes': minute,
    }
    if hour > current_date.hour or (hour == current_date.hour and minute > current_date.minute):
        time.sleep(timedelta(hours=hour - current_date.hour, minutes = minute - current_date.minute).total_seconds())
    else:
        time.sleep(timedelta(**query).total_seconds())


def get_groups():
    groups = []
    
    def group_handler(group: str):
        group = group.replace('https://vk.com/', '')
        if group.startswith('club'):
            group = group.replace('club', '')
        return group

    with open(f'{os.getcwd()}/assets/group.txt') as f:
        for group in f:
           groups.append(group.strip())
    groups = list(map(group_handler, groups))

    return groups


class VK:

    def __init__(self, token, login, password, app_id):
        session = vk_api.VkApi(login, password, token=token, app_id=app_id, auth_handler=self.two_factor_auth, scope='WALL,GROUPS,PHOTOS')
        session.auth()
        self.v = '5.81'
        self.vk = session.get_api()

    @staticmethod
    def two_factor_auth():
        code = input('Please input code for Two factor authentification: ')
        return code, True
    
    def get_group_id(self, group_name):
        r = self.vk.groups.getById(group_ids=group_name, v=self.v)
        return str(r[0]['id'])
        

    def upload(self, photo, owner_id):
        upl = vk_api.VkUpload(self.vk).photo_wall(photo, group_id=owner_id)
        uri = 'photo{}_{}'.format(upl[0]['owner_id'], upl[0]['id'])
        return uri

    def send_wall_post(self, owner_id:str, message, photo):
        if not owner_id.isdigit():
            owner_id = self.get_group_id(owner_id)
        self.vk.wall.post(owner_id='-'+owner_id, message=message, attachments=self.upload(photo, owner_id), v = self.v)
        return
        

if __name__ == "__main__":

    text = open(f'{os.getcwd()}/assets/piar.txt').read()
    app = VK(TOKEN, LOGIN, PWD, APP_ID)

    for group in get_groups():
        query = {
            'owner_id': group,
            'message': text,
            'photo': f"assets/{PHOTO_FILEPATH}"
        }
        set_timer()
        app.send_wall_post(**query)

        # time.sleep()

