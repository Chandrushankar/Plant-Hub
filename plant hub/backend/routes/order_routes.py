from flask import Blueprint, jsonify, request
from database import get_db_connection

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/create', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    cart_items = data.get('items') # List of {plant_id, quantity, price}
    total_amount = data.get('total')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Create Order
        cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, total_amount))
        order_id = cursor.lastrowid
        
        # 2. Insert Order Items
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, plant_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['plant_id'], item['quantity'], item['price']))
            
        conn.commit()
        return jsonify({"message": "Order placed successfully", "order_id": order_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@orders_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        orders = cursor.fetchall()
        return jsonify(orders)
    finally:
        cursor.close()
        conn.close()
