#!/bin/bash

###############################################################################
# Application Deployment Script for Pronunciation Checker
# Run this script on the EC2 instance to deploy the application
###############################################################################

set -e

APP_NAME="pronunciation-checker"
APP_DIR="/home/ubuntu/pronuciation_checker"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="/var/log/$APP_NAME"
SERVICE_NAME="pronunciation-checker"

echo "=========================================="
echo "Deploying Pronunciation Checker Application"
echo "=========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root"
    exit 1
fi

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    supervisor \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Create application directory
echo "Setting up application directory..."
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
fi

cd "$APP_DIR"

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Installing manually..."
    pip install flask flask_cors python-dotenv langchain langchain_core langchain_community langchain_google_genai langgraph werkzeug gunicorn
fi

# Create necessary directories
echo "Creating application directories..."
mkdir -p "$APP_DIR/uploads"
mkdir -p "$APP_DIR/logs"
sudo mkdir -p "$LOG_DIR"
sudo chown -R ubuntu:ubuntu "$LOG_DIR"

# Create .env file if it doesn't exist
if [ ! -f "$APP_DIR/.env" ]; then
    echo "Creating .env file..."
    cat > "$APP_DIR/.env" << 'EOF'
# Google API Key (REQUIRED - Replace with your actual key)
GOOGLE_API_KEY=your_google_api_key_here

# Flask Configuration
SECRET_KEY=your-secret-key-change-this
UPLOAD_FOLDER=./uploads

# Production Settings
FLASK_ENV=production
FLASK_DEBUG=False

# Cleanup Configuration
CLEANUP_ENABLED=true
CLEANUP_MAX_AGE_DAYS=7
CLEANUP_INTERVAL_HOURS=24
EOF
    echo "⚠️  IMPORTANT: Edit .env file and add your Google API key!"
    echo "   Run: nano $APP_DIR/.env"
fi

# Setup cleanup cron job (optional but recommended)
echo "Setting up cleanup cron job..."
CRON_SCRIPT="$APP_DIR/scripts/cleanup_cron.sh"
chmod +x "$CRON_SCRIPT"

# Add cron job if not already present
(crontab -l 2>/dev/null | grep -v "$CRON_SCRIPT"; echo "0 2 * * * $CRON_SCRIPT") | crontab -
echo "✓ Cleanup cron job added (runs daily at 2 AM)"

# Create Gunicorn configuration
echo "Creating Gunicorn configuration..."
cat > "$APP_DIR/gunicorn_config.py" << 'EOF'
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = '/var/log/pronunciation-checker/access.log'
errorlog = '/var/log/pronunciation-checker/error.log'
loglevel = 'info'

# Process naming
proc_name = 'pronunciation-checker'

# Server mechanics
daemon = False
pidfile = '/var/run/pronunciation-checker.pid'
user = 'ubuntu'
group = 'ubuntu'
tmp_upload_dir = None

# SSL (uncomment if using SSL)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'
EOF

# Create systemd service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=Pronunciation Checker Flask Application
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --config gunicorn_config.py run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }

    location /static {
        alias /home/ubuntu/pronuciation_checker/static;
        expires 30d;
    }

    location /uploads {
        alias /home/ubuntu/pronuciation_checker/uploads;
        expires 7d;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Reload systemd and start services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME
sudo systemctl restart nginx

# Check service status
echo ""
echo "Checking service status..."
sudo systemctl status $SERVICE_NAME --no-pager || true

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Application directory: $APP_DIR"
echo "Virtual environment: $VENV_DIR"
echo "Log directory: $LOG_DIR"
echo ""
echo "Service commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. Edit .env file with your Google API key:"
echo "   nano $APP_DIR/.env"
echo "2. Restart the service:"
echo "   sudo systemctl restart $SERVICE_NAME"
echo "3. Test the application:"
echo "   curl http://localhost/api/v1/health-check"
echo "=========================================="
