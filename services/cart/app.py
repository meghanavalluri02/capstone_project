import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    dbname=os.environ['DB_NAME']
)
cur = conn.cursor()

# Create cart table
cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL
    );
""")
conn.commit()

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cur.execute(
        "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s) RETURNING id;",
        (data['user_id'], data['product_id'], data['quantity'])
    )
    conn.commit()
    return jsonify({"id": cur.fetchone()[0]}), 201

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cur.execute("SELECT * FROM cart WHERE user_id = %s;", (user_id,))
    items = cur.fetchall()
    return jsonify(items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
