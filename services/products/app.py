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

# Create products table
cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price NUMERIC NOT NULL
    );
""")
conn.commit()

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;", (name, price))
    conn.commit()
    return jsonify({"id": cur.fetchone()[0]}), 201

@app.route('/products', methods=['GET'])
def get_products():
    cur.execute("SELECT * FROM products;")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
