import aiosqlite

DB = 'database.db'


# create db

async def create_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE , lang VARCHAR(255), balance FLOAT, referals INTENGER, own_id INTEGER UNIQUE, PRIMARY KEY('own_id' AUTOINCREMENT))")
        await db.commit()

async def user_exist(user_id):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute(
            "SELECT EXISTS(SELECT id FROM users WHERE id = {})".format(user_id))
        return await cursor.fetchone()

async def create_user(data):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (id,lang,balance,referals) VALUES (?, ?, ?, ?)", (data, "None",0.00,0))
        await db.commit()

async def change_lang(user_id,lang):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET lang = '{}' WHERE id = {}".format(lang,user_id))
        await db.commit()

async def change_balance(user_id,balance):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET balance = {} WHERE id = {}".format(balance,user_id))
        await db.commit()

async def change_referalse(user_id):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET referals = referals + 1 WHERE id = {}".format(user_id))
        await db.commit()


async def get_user_data(user_id):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT * from users WHERE id = {}".format(user_id))
        return await cursor.fetchone()

async def get_lang(user_id):
   async with aiosqlite.connect(DB) as db:
       cursor = await db.execute("SELECT lang from users WHERE id = {}".format(user_id))
       cursor = await cursor.fetchone()
       return cursor[0]

async def get_user_count():
     async with aiosqlite.connect(DB) as db:
       cursor = await db.execute("SELECT COUNT(*) FROM users")
       cursor = await cursor.fetchone()
       return cursor[0]

async def get_max_balance():
     async with aiosqlite.connect(DB) as db:
       cursor = await db.execute("SELECT MAX(balance) from users")
       cursor = await cursor.fetchone()
       return cursor[0]

async def get_balance(user_id):
    async with aiosqlite.connect(DB) as db:
       cursor = await db.execute("SELECT balance from users WHERE id = {}".format(user_id))
       cursor = await cursor.fetchone()
       return cursor[0]

