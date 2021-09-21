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

AT_TIME = ['17:00']

DELAY = 5  # Delay between posts in minutes

BYPASS_TIMER = False

def set_timer(callback, props:dict, time_array:list):    
    while True:
        current_date = datetime.today()

        hour = current_date.hour
        minute = current_date.minute
        if len(str(minute)) == 1:
            minute = f'0{current_date.minute}'
        
        print(f'{hour}:{minute}')
        
        if f'{hour}:{minute}' in time_array:
            if props:
                callback(**props)
                return


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
        try:
            self.vk.wall.post(owner_id='-'+owner_id, message=message, attachments=self.upload(photo, owner_id), v = self.v)
            print("Пост отправлен")
        except:
            print("Что-то пошло не так")
        return
        

if __name__ == "__main__":

    text = open(f'{os.getcwd()}/assets/piar.txt', encoding='utf-8').read()
    app = VK(TOKEN, LOGIN, PWD, APP_ID)
    while True:
        for idx, group in enumerate(get_groups()):
            query = {
                'owner_id': group,
                'message': text,
                'photo': f"assets/{PHOTO_FILEPATH}"
            }
            if not BYPASS_TIMER and idx == 0: 
                set_timer(app.send_wall_post, query, AT_TIME)
            else:
                app.send_wall_post(**query)
            time.sleep(DELAY*60)

