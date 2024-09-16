from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Encrypted message
    expiration = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now() + timedelta(hours=1))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def is_expired(self):
        return datetime.now() > self.expiration
