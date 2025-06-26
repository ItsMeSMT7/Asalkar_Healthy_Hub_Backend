# backend/app.py

from flask import Flask, request, send_file
from flask_cors import CORS  # Make sure this import is here
import os
import qrcode
import io


# Initialize the Flask app as before
app = Flask(__name__, static_folder="../static")

# ✅ THE DEFINITIVE FIX: Apply CORS to the entire app.
# This is the most direct way to tell Flask: "For every single route in this
# application, add the 'Access-Control-Allow-Origin: *' header."
CORS(app) 

# ✅ IMPORTANT: Add this line to tell Flask where to save uploaded product images.
# Make sure the 'static/images/products' directory exists.
app.config['UPLOAD_FOLDER'] = 'static/images/products'

# --- Import and Register Blueprints ---
# (The rest of the file remains the same)
from routes.auth_routes import auth_bp
from routes.order_routes import order_bp
from routes.product_routes import product_bp
from routes.admin_routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(admin_bp)

@app.route('/generate_qr')
def generate_qr():
    upi_id = request.args.get('upi_id')
    name = request.args.get('name')
    amount = request.args.get('amount')
    note = request.args.get('note', 'Asalkar Healthy Hub Order')

    if not upi_id or not amount:
        return "Missing UPI ID or Amount", 400

    # UPI Payment URL
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}"

    # Generate QR
    qr = qrcode.make(upi_link)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

@app.route("/")
def home():
    return "✅ Asalkar Healthy Hub Backend Running"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
if __name__ == "__main__":
    # Ensure the upload folder exists when the app starts
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5000)