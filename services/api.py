import requests
import re
import aiohttp

from settings.database import Database


class Api:
    def __init__(self):
        self.base_url = 'https://2d8d-31-16-251-190.ngrok-free.app/'

    async def registration(self, email, password1, password2):
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

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 201:
                    return True
                else:
                    return False

    async def authorization(self, email, password):
        endpoint = 'api/auth/login/'
        url = self.base_url + endpoint
        print(email, password)

        payload = {
            "email": email,
            "password": password,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                print(await response.json())
                if response.status == 200:
                    return await response.json()
                else:
                    return False


    async def auty(self, user_id, session, refresh_token):
        print('Token expired')
        refresh_endpoint = 'api/auth/token/refresh/'
        url = self.base_url + refresh_endpoint
        print(f'Refresh token: {refresh_token}')

        payload = {
            "refresh": refresh_token
        }
        async with session.post(url, json=payload) as refresh_response:
            if refresh_response.status == 200:
                data = await refresh_response.json()
                access_token = data['access']
                print('Access token below')
                print(access_token)
                refresh_token = data['refresh']
                await Database.save_user(user_id=user_id, email=None,
                                         access_token=access_token, refresh_token=refresh_token)

                return await refresh_response
            elif refresh_response.status == 401:
                print('Refresh request failed')
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
                    await self.auty(user_id, session, refresh_token)
                    return await self.get_something(user_id, access_token, refresh_token, endpoint)
                else:
                    print(f"Error: {response.status}")
                    return None


    async def save_something(self, user_id, access_token, refresh_token, endpoint, form_data):
        url = self.base_url + endpoint

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as response:
                if response.status == 201:
                    print('All good')
                    return await response.json()
                elif response.status == 401:
                    await self.auty(user_id, session, refresh_token)
                    return await self.save_something(user_id, access_token, refresh_token, endpoint, form_data)
                else:
                    print(f"Error: {response.status}")
                    return False
