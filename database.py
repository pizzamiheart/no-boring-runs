import psycopg2
import os
from psycopg2.extras import RealDictCursor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT']
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        strava_token VARCHAR(100)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS journeys (
        username VARCHAR(50) PRIMARY KEY,
        total_miles FLOAT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        current_position POINT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        distance FLOAT NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        stored_password = result[1]
        print(f"Stored password: {stored_password}, Provided password: {password}")
        password_match = stored_password == password
        print(f"Password match result: {password_match}")
        logger.info(f"User {username} authenticated successfully")
        return password_match
    else:
        logger.warning(f"Authentication failed for user {username}")
        return False

def user_exists(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def create_user(username, password, strava_connect):
    conn = get_db_connection()
    cur = conn.cursor()
    strava_token = 'pending' if strava_connect else None
    cur.execute("INSERT INTO users (username, password, strava_token) VALUES (%s, %s, %s)", (username, password, strava_token))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"User {username} created successfully")

def create_user_journey(username, total_miles, start_date, end_date, start_position):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO journeys (username, total_miles, start_date, end_date, current_position)
    VALUES (%s, %s, %s, %s, POINT(%s, %s))
    """, (username, total_miles, start_date, end_date, start_position[0], start_position[1]))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Journey created for user {username}")

def get_user_journey(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT total_miles, start_date, end_date, current_position
    FROM journeys WHERE username = %s
    """, (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def add_run(username, distance, date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO runs (username, distance, date)
    VALUES (%s, %s, %s)
    """, (username, distance, date))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Run added for user {username}")

def get_user_runs(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT distance, date FROM runs WHERE username = %s ORDER BY date DESC", (username,))
    runs = cur.fetchall()
    cur.close()
    conn.close()
    return runs

def update_user_position(username, new_position):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    UPDATE journeys SET current_position = POINT(%s, %s)
    WHERE username = %s
    """, (new_position[0], new_position[1], username))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Updated position for user {username}")

def get_user_data(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password, strava_token FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        logger.info(f"User data retrieved for {username}")
    else:
        logger.warning(f"No user data found for {username}")
    return result

# Initialize the database
init_db()