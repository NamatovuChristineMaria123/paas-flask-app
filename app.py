from flask import Flask, render_template
from datetime import datetime
import socket
import os
import platform
import uuid
import psycopg2

app = Flask(__name__)

# Connect to Railway PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id SERIAL PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100)
)
""")
conn.commit()

@app.route("/")
def home():
    session_id = str(uuid.uuid4())[:8]

    return render_template('index.html',
                         current_time=datetime.now().strftime("%H:%M:%S"),
                         current_date=datetime.now().strftime("%B %d, %Y"),
                         hostname=socket.gethostname(),
                         platform_info=platform.python_version(),
                         session_id=session_id,
                         message="Your application is running inside a Docker container deployed on Railway")

@app.route("/add")
def add_user():
    cursor.execute(
        "INSERT INTO users (name,email) VALUES (%s,%s)",
        ("Christine","christine@email.com")
    )
    conn.commit()
    return "User added!"

@app.route("/users")
def view_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return str(users)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)