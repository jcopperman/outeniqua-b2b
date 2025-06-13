# Outeniqua Studios Contact Form Backend

A minimal Flask backend for handling contact form submissions from the Outeniqua Studios website.

## Setup

1. Create and activate a Python virtual environment:
```bash
cd /var/www/outeniqua-b2b/backend
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure and install the systemd service:
```bash
sudo cp outeniqua-contact.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable outeniqua-contact.service
sudo systemctl start outeniqua-contact.service
```

3. Configure your web server (Nginx example):
```nginx
location /backend/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Testing

You can test the API with curl:

```bash
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","message":"This is a test message from the API"}'
```

## Features

- Validates form input including email format
- Sends emails via local SMTP server
- Provides clear error messages
- Returns JSON responses for frontend integration
