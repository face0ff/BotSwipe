import aiohttp

async def get_address_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                address = data.get('display_name')
                return address
            else:
                return None


import aiohttp

async def get_coordinates_from_address(address):
    url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&q={address}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    latitude = float(data[0]['lat'])
                    longitude = float(data[0]['lon'])
                    return latitude, longitude
                else:
                    return None
            else:
                return None