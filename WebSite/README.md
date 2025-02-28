# QR Authentication System

A lightweight two-interface web application for QR-based authentication with enhanced token management and visual features.

## Features

- User registration and login
- QR code generation for users
- Token-based authentication
- Verifier portal for scanning and validating QR codes
- Visual status indicators for token redemption
- Responsive design

## Tech Stack

- Backend: Flask (Python)
- Frontend: Vanilla JavaScript
- UI Framework: Bootstrap 5 (Dark Theme)
- QR Code: qrcode.js (generation) and HTML5-QRCode (scanning)

## Setup

1. Install dependencies:
```bash
pip install flask flask-sqlalchemy requests werkzeug
```

2. Set environment variables:
```bash
SESSION_SECRET=your_secret_key
API_BASE_URL=your_api_base_url
```

3. Run the application:
```bash
python main.py
```

The server will start on `http://localhost:5000`

## Project Structure

```
├── static/
│   ├── css/
│   │   └── custom.css       # Custom styles
│   └── js/
│       ├── qr.js           # QR code generation
│       └── scanner.js      # QR code scanning
├── templates/
│   ├── base.html          # Base template
│   ├── dashboard.html     # User dashboard
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── verifier.html      # Verifier portal
├── app.py                 # Flask app initialization
├── config.json            # Verifier credentials
├── main.py               # Application entry point
└── routes.py             # Route handlers
```

## Usage

1. Register as a new user
2. Login with your credentials
3. View your QR code in the dashboard
4. Use the verifier portal to scan QR codes
   - Login credentials: username: `admin`, password: `admin`

## Token Status

- Active tokens: Green border
- Redeemed tokens: Red border

## Security Notes

- For production deployment:
  - Change default verifier credentials
  - Use secure session management
  - Enable HTTPS
  - Implement rate limiting
