import psycopg2
import os
from psycopg2.extras import RealDictCursor

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
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

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

def recreate_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute('''
    CREATE TABLE users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        strava_token VARCHAR(100)
    )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialize the database
init_db()

# Uncomment the following line to recreate the users table
recreate_users_table()
