from flask import Flask, request, jsonify
from models import db, Message
from utils import encrypt_message, decrypt_message
from datetime import datetime, timedelta
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://SDT:SDT@localhost/SDT'
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json
    message = data.get("message")
    expiration_time = int(data.get("expiration", 3600))  # Default: 1 hour

    # Encrypt the message
    encrypted = encrypt_message(message)

    # Store in DB
    expiration = datetime.now() + timedelta(seconds=expiration_time)
    db_message = Message(content=encrypted["ciphertext"], expiration=expiration)
    db.session.add(db_message)
    db.session.commit()

    # Construct URL with GET parameters (IV, Tag, and ID)
    decrypt_url = f"http://localhost:5173/decrypt?id={db_message.id}&iv={encrypted['iv']}&tag={encrypted['tag']}"

    return jsonify({
        "key": encrypted["key"],  # Separately provide the key
        "url": decrypt_url  # URL for decryption with necessary params
    }), 200

@app.route("/decrypt/<int:id>", methods=["POST"])
def decrypt(id):
    data = request.json
    key = data.get("key")
    iv = data.get("iv")
    tag = data.get("tag")

    # Retrieve message from DB
    message = Message.query.get(id)
    if not message or message.is_expired():
        return jsonify({"error": "Message not found or expired"}), 404

    decrypted = decrypt_message(message.content, key, iv, tag)
    return jsonify({"message": decrypted.decode()})

if __name__ == "__main__":
    app.run(debug=True)
