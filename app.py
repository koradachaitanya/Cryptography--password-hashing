import os
from flask import Flask, render_template, request, jsonify
import bcrypt
from cryptography.fernet import Fernet

app = Flask(__name__)

# Load Fernet key from environment variable or generate a new one
FERNET_KEY = os.environ.get('FERNET_KEY')
if not FERNET_KEY:
    # Generate a key and print it for first-time setup
    FERNET_KEY = Fernet.generate_key()
    print("Generated new Fernet key (save this for future use):", FERNET_KEY.decode())
fernet = Fernet(FERNET_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    text = data.get('text', '')
    try:
        ciphertext = fernet.encrypt(text.encode())
        return jsonify(result=ciphertext.decode())
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    text = data.get('text', '')
    try:
        plaintext = fernet.decrypt(text.encode()).decode()
        return jsonify(result=plaintext)
    except Exception as e:
        return jsonify(error="Invalid ciphertext or decryption error."), 400

@app.route('/hash', methods=['POST'])
def hash_password():
    data = request.get_json()
    password = data.get('password', '')
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return jsonify(result=hashed.decode('utf-8', errors='ignore'))
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/verify', methods=['POST'])
def verify_password():
    data = request.get_json()
    password = data.get('password', '')
    hash_str = data.get('hash', '')
    try:
        hashed = hash_str.encode('utf-8')
        match = bcrypt.checkpw(password.encode(), hashed)
        return jsonify(result=match)
    except Exception as e:
        return jsonify(error="Invalid hash or password."), 400 

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

if __name__ == '__main__':
    app.run(debug=True)