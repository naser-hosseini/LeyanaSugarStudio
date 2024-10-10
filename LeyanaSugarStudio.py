from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# PostgreSQL connection settings
db_config = {
    'dbname': 'LeyanaSugarStudio',
    'user': '****',
    'password': '****',
    'host': 'localhost',
    'port': '5432'
}

# Function to get a connection to the database
def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

# POST endpoint for purchasing ingredient history
@app.route('/purchase_ingredient', methods=['POST'])
def purchase_ingredient():
    data = request.json
    ingredient_name = data.get('ingredient_name')
    quantity = data.get('quantity')
    purchase_date = data.get('purchase_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL("INSERT INTO ingredient_history (ingredient_name, quantity, purchase_date) VALUES (%s, %s, %s)")
    cursor.execute(query, (ingredient_name, quantity, purchase_date))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Ingredient purchase history added successfully."}), 201

# POST endpoint for storing customer info
@app.route('/store_customer', methods=['POST'])
def store_customer():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL("INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)")
    cursor.execute(query, (name, email, phone))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer info added successfully."}), 201

# POST endpoint for extracting ingredients from the database
@app.route('/extract_ingredient', methods=['POST'])
def extract_ingredient():
    data = request.json
    ingredient_name = data.get('ingredient_name')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL("SELECT * FROM ingredients WHERE ingredient_name = %s")
    cursor.execute(query, (ingredient_name,))
    ingredients = cursor.fetchall()

    cursor.close()
    conn.close()

    if ingredients:
        return jsonify({"ingredients": ingredients}), 200
    else:
        return jsonify({"message": "Ingredient not found."}), 404

# POST endpoint for selling history
@app.route('/sell_history', methods=['POST'])
def sell_history():
    data = request.json
    item_name = data.get('item_name')
    quantity_sold = data.get('quantity_sold')
    sell_date = data.get('sell_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL("INSERT INTO sell_history (item_name, quantity_sold, sell_date) VALUES (%s, %s, %s)")
    cursor.execute(query, (item_name, quantity_sold, sell_date))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Sell history added successfully."}), 201

# GET endpoint for retrieving purchase ingredient history
@app.route('/get_purchase_ingredient', methods=['GET'])
def get_purchase_ingredient():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingredient_history")
    ingredients = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"ingredients": ingredients}), 200

# GET endpoint for retrieving customer info
@app.route('/get_customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"customers": customers}), 200

# GET endpoint for retrieving ingredient data
@app.route('/get_ingredient', methods=['GET'])
def get_ingredient():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingredients")
    ingredients = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"ingredients": ingredients}), 200

# GET endpoint for retrieving sell history
@app.route('/get_sell_history', methods=['GET'])
def get_sell_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sell_history")
    sales = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"sales": sales}), 200

if __name__ == '__main__':
    app.run(debug=True)
