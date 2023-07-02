import motor.motor_asyncio


class Database:
    client = None
    database_name = 'swipe'

    @classmethod
    async def connect(cls):
        cls.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
        return cls.client

    @classmethod
    def get_database(cls):
        return cls.client[cls.database_name]

    async def save_user(user_id, email, password, refresh_token, access_token):
        client = await Database.connect()
        db = client.users

        user_data = await db.users.find_one({'user_id': user_id})

        if user_data:
            # Пользователь найден, обновляем email и password
            if email:
                user_data['email'] = email
            if password:
                user_data['password'] = password
            if refresh_token:
                user_data['refresh_token'] = refresh_token
            if access_token:
                user_data['access_token'] = access_token
            await db.users.update_one({'user_id': user_id}, {'$set': user_data})
        else:
            # Пользователь не найден, создаем нового
            user_data = {
                'user_id': user_id,
                'refresh_token': refresh_token,
                'access_token': access_token,
                'email': email,
                'password': password,
            }
            await db.users.insert_one(user_data)

        return user_data


