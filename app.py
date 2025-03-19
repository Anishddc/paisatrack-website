from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from validate_email import validate_email
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscribers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db = SQLAlchemy(app)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_subscribed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Subscriber {self.email}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Validate email format
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Check if email already exists
    if Subscriber.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already subscribed'}), 409

    try:
        # Add subscriber to database
        new_subscriber = Subscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()

        # Send thank you email
        msg = Message(
            'Welcome to Paisa Track!',
            recipients=[email]
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1a75ff;">Thank You for Subscribing!</h2>
            <p>Dear Future User,</p>
            <p>Thank you for your interest in Paisa Track! We're excited to have you join our community. You'll be among the first to know when we launch our app.</p>
            <p>What to expect:</p>
            <ul>
                <li>Launch notification</li>
                <li>Early access opportunities</li>
                <li>Special offers for early subscribers</li>
            </ul>
            <p>Stay tuned for updates!</p>
            <p>Best regards,<br>The Paisa Track Team</p>
            <div style="margin-top: 20px; font-size: 12px; color: #666;">
                <p>If you didn't subscribe to Paisa Track, please ignore this email.</p>
            </div>
        </div>
        """
        mail.send(msg)

        return jsonify({
            'message': 'Successfully subscribed! Please check your email for confirmation.'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
