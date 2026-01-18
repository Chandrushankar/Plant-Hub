from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from database import get_db_connection

# Import Blueprints
from routes.plants_routes import plants_bp
from routes.cart_routes import cart_bp
from routes.order_routes import orders_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(plants_bp, url_prefix='/api/plants')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

# Firebase Setup
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Warning: Firebase Admin not initialized. Error: {e}")

@app.route('/')
def home():
    return jsonify({"message": "Plant Hub API is running 🌿", "status": "active", "version": "2.0 (Modular)"})

# Auth Route (Kept here for simplicity, could be moved to auth_routes.py)
@app.route('/api/auth/verify', methods=['POST'])
def verify_user():
    data = request.json
    id_token = data.get('token')
    
    # Verify Token
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        user_data = {
            "uid": decoded_token.get('uid'),
            "email": decoded_token.get('email'),
            "phone": decoded_token.get('phone_number')
        }
    except Exception as e:
        # Demo fallback
        if id_token == "mock_token_123":
            user_data = {"uid": "mock_uid", "email": "demo@example.com"}
        else:
            return jsonify({"error": "Invalid token"}), 401

    # Upsert User in MySQL
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            provider = 'phone' if user_data.get('phone') else 'email/google'
            sql = """
            INSERT INTO users (firebase_uid, email, phone, auth_provider) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            email = VALUES(email), phone = VALUES(phone)
            """
            cursor.execute(sql, (user_data['uid'], user_data.get('email'), user_data.get('phone'), provider))
            conn.commit()
        except Exception as e:
            print(f"DB Error: {e}")
        finally:
            cursor.close()
            conn.close()
        
    return jsonify({"message": "User verified", "user": user_data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
