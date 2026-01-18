from flask import Blueprint, jsonify, request
from database import get_db_connection
# In a real app, importing verify_token middleware would happen here

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
        SELECT c.id, c.quantity, p.plant_name, p.price, p.image_url 
        FROM cart c
        JOIN plants p ON c.plant_id = p.id
        WHERE c.user_id = %s
        """
        cursor.execute(sql, (user_id,))
        items = cursor.fetchall()
        return jsonify(items)
    finally:
        cursor.close()
        conn.close()

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    plant_id = data.get('plant_id')
    quantity = data.get('quantity', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if item already exists in cart, update quantity if so
        cursor.execute("SELECT id, quantity FROM cart WHERE user_id = %s AND plant_id = %s", (user_id, plant_id))
        existing = cursor.fetchone()
        
        if existing:
            new_qty = existing[1] + quantity
            cursor.execute("UPDATE cart SET quantity = %s WHERE id = %s", (new_qty, existing[0]))
        else:
            cursor.execute("INSERT INTO cart (user_id, plant_id, quantity) VALUES (%s, %s, %s)", (user_id, plant_id, quantity))
            
        conn.commit()
        return jsonify({"message": "Item added to cart"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@cart_bp.route('/remove/<int:cart_id>', methods=['DELETE'])
def remove_item(cart_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
        conn.commit()
        return jsonify({"message": "Item removed"})
    finally:
        cursor.close()
        conn.close()
