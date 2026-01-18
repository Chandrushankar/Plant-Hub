from flask import Blueprint, jsonify, request
from database import get_db_connection

plants_bp = Blueprint('plants', __name__)

@plants_bp.route('/', methods=['GET'])
def get_all_plants():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch plants with essential info
        cursor.execute("SELECT * FROM plants")
        plants = cursor.fetchall()
        return jsonify(plants)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@plants_bp.route('/<int:plant_id>', methods=['GET'])
def get_plant_details(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get core plant details
        cursor.execute("SELECT * FROM plants WHERE id = %s", (plant_id,))
        plant = cursor.fetchone()
        
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
            
        # Get care details
        cursor.execute("SELECT * FROM plant_care WHERE plant_id = %s", (plant_id,))
        care = cursor.fetchone()
        
        # Merge data
        plant['care_guide'] = care if care else {}
        
        return jsonify(plant)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
