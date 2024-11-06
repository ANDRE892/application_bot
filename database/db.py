import asyncpg

# ================================
from randoms.randoms import generate_ticket
from hendlers.group import message_group
# --------------------------------


async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres',
        password='admin',
        database='test_task',
        port=5432,
        host='localhost'
    )


async def create_user():
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            name_surname TEXT
            )
            """
        )
    finally:
        await pool.release(conn)


async def create_application():
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS application (
            user_id BIGINT,
            application TEXT,
            ticket TEXT,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            topic TEXT
            )
            """
        )
    finally:
        await pool.release(conn)


async def create_email():
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS email (
            topic TEXT UNIQUE,
            email_come TEXT,
            pass TEXT,
            email_where TEXT
            )
            """
        )
    finally:
        await pool.release(conn)


async def completion_email():
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            INSERT INTO email (topic, email_come, pass, email_where) 
            VALUES 
                ('chancellery', '', '', ''), 
                ('software', '', '', ''), 
                ('topic', '', '', '')
            ON CONFLICT (topic) DO NOTHING
            """
        )
    finally:
        await pool.release(conn)


async def exists(user_id):
    conn = await pool.acquire()
    try:
        result = await conn.fetchrow(
            """
            SELECT user_id 
            FROM users 
            WHERE user_id = $1""",
            user_id)
        return result is not None
    finally:
        await pool.release(conn)


async def new_user(user_id, name_surname):
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            INSERT INTO users (user_id, name_surname) 
            VALUES ($1, $2)
            """,
            user_id, name_surname)
    finally:
        await pool.release(conn)


async def applications_save(user_id, text, topic):
    conn = await pool.acquire()
    try:
        ticket = generate_ticket()
        await conn.execute(
            """
            INSERT INTO application (user_id, application, ticket, status, timestamp, topic) 
            VALUES ($1, $2, $3, 'check', CURRENT_TIMESTAMP, $4)
            """,
            user_id, text, ticket, topic
        )
        await message_group(user_id, text, topic, ticket)
    finally:
        await pool.release(conn)


async def history_bid(user_id):
    conn = await pool.acquire()
    try:
        result = await conn.fetch(
            """
            SELECT application, status 
            FROM application 
            WHERE user_id = $1 
            ORDER BY timestamp ASC 
            LIMIT 30
            """,
            user_id
        )
        return result
    finally:
        await pool.release(conn)


async def replacement_email(password, email, topic):
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            UPDATE email 
            SET email_come = $1, pass = $2 
            WHERE topic = $3
            """,
            email, password, topic
        )
    finally:
        await pool.release(conn)


async def incoming_email(email):
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            UPDATE email 
            SET email_where = $1
            """,
            email
        )
    finally:
        await pool.release(conn)


async def thirty_application():
    conn = await pool.acquire()
    try:
        result = await conn.fetch(
            """
            SELECT user_id, application, ticket, status, timestamp, topic 
            FROM application 
            ORDER BY timestamp DESC 
            LIMIT 30
            """
        )
        return result
    finally:
        await pool.release(conn)


async def find_application(ticket):
    conn = await pool.acquire()
    try:
        results = await conn.fetch(
            """
            SELECT user_id, application, status, timestamp, topic 
            FROM application 
            WHERE ticket = $1
            """, ticket
        )
        return results
    finally:
        await pool.release(conn)


async def unfinished_application():
    conn = await pool.acquire()
    try:
        result = await conn.fetch(
            """
            SELECT user_id, application, ticket, timestamp, topic 
            FROM application 
            WHERE status = 'check'
            """
        )
        return result
    finally:
        await pool.release(conn)


async def get_email(topic):
    conn = await pool.acquire()
    try:
        result = await conn.fetchrow(
            """
            SELECT email_where, email_come, pass 
            FROM email 
            WHERE topic = $1
            """,
            topic
        )
        return result
    finally:
        await pool.release(conn)


async def true_application(status, ticket):
    conn = await pool.acquire()
    try:
        await conn.execute(
            """
            UPDATE application 
            SET status = $1 
            WHERE ticket = $2
            """,
            status, ticket
        )
    finally:
        await pool.release(conn)


async def ticket_user_id(ticket):
    conn = await pool.acquire()
    try:
        result = await conn.fetchval(
            """
            SELECT user_id 
            FROM application 
            WHERE ticket = $1
            """,
            ticket
        )
        return result
    finally:
        await pool.release(conn)


async def duplicate_ticket(ticket):
    conn = await pool.acquire()
    try:
        result = await conn.fetch(
            """
            SELECT user_id, application, topic 
            FROM application 
            WHERE ticket = $1
            """, ticket
        )

        if result:
            user_id = result[0]["user_id"]
            application = result[0]["application"]
            topic = result[0]["topic"]

            await message_group(user_id, text=application, topic=topic, ticket=ticket)
            return True
        else:
            return False

    finally:
        await pool.release(conn)
