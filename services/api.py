import requests
import re
import aiohttp


from settings.database import Database


class Api:
    def __init__(self):
        self.base_url = 'https://2914-31-16-251-190.ngrok-free.app/'

    def registration(self, email, password1, password2):
        endpoint = 'api/v1/user_register/'
        url = self.base_url + endpoint
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            return 'email'

        if password1 != password2:
            return 'pass'

        payload = {
            "email": email,
            "password1": password1,
            "password2": password2,
            "first_name": "string",
            "last_name": "string"
        }

        response = requests.post(url, json=payload)
        if response.status_code == 201:
            return True
        else:
            return False

    def authorization(self, email, password):
        endpoint = 'api/auth/login/'
        url = self.base_url + endpoint

        payload = {
            "email": email,
            "password": password,
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response
        else:
            return False


    async def get_something(self, user_id, access_token, refresh_token, endpoint):
        print(refresh_token)
        url = self.base_url + endpoint

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    print('token expired')
                    endpoint = 'api/auth/token/refresh/'
                    url = self.base_url + endpoint

                    payload = {
                        "refresh": refresh_token
                    }
                    async with session.post(url, json=payload) as refresh_response:
                        if response.status == 200:
                            data = await refresh_response.json()
                            access_token = data['access']
                            refresh_token = data['refresh']
                            await Database.save_user(user_id=user_id, email=None, password=None,
                                                     access_token=access_token, refresh_token=refresh_token)

                            return await refresh_response.json()
                        elif response.status == 401:
                            return False
                else:
                    print(f"Error: {response.status}")
                    return None

