import os
import logging
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config["API_BASE_URL"] = os.environ.get(
    "API_BASE_URL", "http://127.0.0.1:8000")

# Import routes after app is created to avoid circular imports
import routes  # noqa: E402
