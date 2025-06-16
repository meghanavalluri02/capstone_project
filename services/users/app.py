import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to PostgreSQL (AWS RDS)
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    dbname=os.environ['DB_NAME']
)
cur = conn.cursor()

# Create users table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE
    );
""")
conn.commit()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
    conn.commit()
    new_id = cur.fetchone()[0]
    return jsonify({"id": new_id}), 201

@app.route('/users', methods=['GET'])
def list_users():
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
