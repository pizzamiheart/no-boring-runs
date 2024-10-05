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
        strava_token JSON
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_user(username, password, strava_token=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, strava_token) VALUES (%s, %s, %s)", 
                (username, password, strava_token))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"User {username} created successfully")

def get_user_data(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, password, strava_token FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def update_strava_token(username, strava_token):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET strava_token = %s WHERE username = %s", 
                (strava_token, username))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Strava token updated for user {username}")

# Keep other existing functions (authenticate_user, add_run, get_user_runs, etc.)

# Initialize the database
init_db()
