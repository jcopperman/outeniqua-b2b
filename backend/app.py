from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import re
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
CORS(app)

# Email configuration
SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 587
SMTP_USER = "jonathan@outeniquastudios.com"
SMTP_PASSWORD = "Limerance12@"
RECIPIENT_EMAIL = "jonathan@outeniquastudios.com"

def validate_inputs(name, email, message):
    errors = []
    
    # Validate name
    if not name or len(name.strip()) < 2:
        errors.append("Name is required (minimum 2 characters)")
    
    # Validate email
    if not email:
        errors.append("Email is required")
    else:
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            errors.append("Please provide a valid email address")
    
    # Validate message
    if not message or len(message.strip()) < 10:
        errors.append("Message is required (minimum 10 characters)")
    
    return errors

def send_email(name, email, message):
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
    
    msg["Subject"] = f"Website Contact: {name}"
    msg["From"] = SMTP_USER
    msg["To"] = RECIPIENT_EMAIL
    msg["Reply-To"] = email
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True, "Message sent successfully"
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, f"Failed to send message: {str(e)}"

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        
        # Extract and sanitize inputs
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        
        # Validate inputs
        errors = validate_inputs(name, email, message)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        
        # Send email
        success, msg = send_email(name, email, message)
        
        if success:
            return jsonify({"success": True, "message": "Thank you for your message. We'll be in touch soon!"}), 200
        else:
            return jsonify({"success": False, "message": "Sorry, there was a problem sending your message."}), 500
            
    except Exception as e:
        print(f"Error processing contact form: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
