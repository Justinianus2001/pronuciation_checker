# Pronunciation Checker

AI-powered English pronunciation analysis application using Google Gemini 2.0 Flash.

## Features

- 🎤 **Pronunciation Error Detection** - Identify mispronounced or omitted words
- 📊 **IELTS Speaking Metrics** - Evaluate fluency, lexical resource, grammar, and pronunciation
- 📝 **Speaking Reports** - Generate comprehensive performance reports
- 🎵 **Audio Support** - MP3, WAV, WebM formats (max 16MB)
- 🧹 **Auto Cleanup** - Automatic deletion of old uploads (7-day retention)

## Tech Stack

- **Backend**: Flask + Python 3.11
- **AI**: Google Gemini 2.0 Flash via LangChain
- **Server**: Gunicorn + Nginx (production)
- **Deployment**: AWS EC2, Docker, CloudFormation

---

## Quick Start

### Prerequisites

1. **Google API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Python 3.11+** or **Docker**

### Local Development

```bash
# 1. Clone repository
git clone <your-repo-url>
cd pronuciation_checker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your GOOGLE_API_KEY

# 5. Run application
python run.py

# 6. Test
curl http://localhost:5000/api/v1/health-check
```

### Docker Deployment

```bash
# 1. Configure environment
cp .env.example .env
nano .env  # Add your GOOGLE_API_KEY

# 2. Deploy
bash scripts/deploy_docker.sh

# 3. Access
curl http://localhost:5000/api/v1/health-check
```

---

## AWS Deployment

### Option 1: EC2 (Recommended for Beginners)

```bash
# 1. Setup infrastructure
bash scripts/setup_ec2.sh

# 2. SSH to instance
ssh -i pronunciation-checker-key.pem ubuntu@YOUR_IP

# 3. Upload code and deploy
bash scripts/deploy_app.sh

# 4. Configure API key
nano /home/ubuntu/pronuciation_checker/.env

# 5. Restart
sudo systemctl restart pronunciation-checker
```

### Option 2: CloudFormation

```bash
bash scripts/deploy_cloudformation.sh
```

**Cost**: ~$18-22/month (FREE with AWS Free Tier for 12 months)

---

## API Endpoints

### Analyze Pronunciation Errors

```bash
POST /api/v1/analyze-pronunciation-error
Content-Type: multipart/form-data

Parameters:
  - audio: file (mp3/wav/webm)
  - text: string (reference text)

Response:
{
  "status": "success",
  "data": {
    "errors": [
      {
        "word": "example",
        "position": 0,
        "error_type": "phát âm sai",
        "correct_pronunciation": "/ɪɡˈzæmpəl/",
        "your_pronunciation": "/ɪɡˈzɑːmpəl/",
        "explanation": "Nguyên âm sai..."
      }
    ],
    "html_output": "<span>...</span>"
  }
}
```

### Evaluate Speech Metrics

```bash
POST /api/v1/evaluate-speech-metrics
Content-Type: multipart/form-data

Parameters:
  - audio: file
  - text: string

Response:
{
  "status": "success",
  "data": {
    "fluency_and_coherence": {
      "score": 7,
      "feedback": "..."
    },
    "lexical_resource": {
      "score": 6,
      "feedback": "..."
    },
    "grammatical_range_and_accuracy": {
      "score": 7,
      "feedback": "..."
    },
    "pronunciation": {
      "score": 6,
      "feedback": "..."
    }
  }
}
```

### Generate Speaking Report

```bash
POST /api/v1/generate-speaking-report
Content-Type: application/x-www-form-urlencoded

Parameters:
  - text: string (test results)

Response:
{
  "status": "success",
  "data": {
    "overall_assessment": "...",
    "common_errors": [...],
    "improvement_suggestions": [...]
  }
}
```

### Storage Management

```bash
# Get storage statistics
GET /api/v1/storage-stats

# Manual cleanup
POST /api/v1/cleanup-uploads
Content-Type: application/json
{"max_age_days": 7}

# Health check
GET /api/v1/health-check
```

---

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
SECRET_KEY=your-secret-key
UPLOAD_FOLDER=./uploads

# Cleanup (defaults shown)
CLEANUP_ENABLED=true
CLEANUP_MAX_AGE_DAYS=7
CLEANUP_INTERVAL_HOURS=24
```

---

## File Upload Flow

### Current Implementation (In-Memory Processing)

```
Client Upload → Validate → Read to RAM → Base64 → Gemini API → Response → Discard
```

**Files are NOT saved to disk by default** for:
- 🚀 Better performance (no disk I/O)
- 🔒 Enhanced privacy (files don't persist)
- 💾 Zero storage usage

### To Enable File Saving

Uncomment line 33 in `app/routes/api.py`:

```python
# Change from:
# audio_path = save_uploaded_file(audio_file)

# To:
audio_path = save_uploaded_file(audio_file)
```

Then files will be saved to `./uploads/` and automatically cleaned up after 7 days.

---

## Automatic Cleanup System

### Features

- 🤖 **Automatic** - Runs every 24 hours
- 🗑️ **Smart** - Deletes files older than 7 days
- 📊 **Monitored** - API endpoints for stats
- 🔄 **Redundant** - Background scheduler + cron job

### How It Works

1. App starts → Cleanup runs immediately
2. Every 24 hours → Cleanup runs automatically
3. Files older than 7 days → Deleted
4. Empty directories → Removed
5. All operations → Logged

### Configuration

```bash
CLEANUP_ENABLED=true              # Enable/disable
CLEANUP_MAX_AGE_DAYS=7           # Delete after X days
CLEANUP_INTERVAL_HOURS=24        # Run every X hours
```

### Monitoring

```bash
# View logs
sudo journalctl -u pronunciation-checker | grep -i cleanup

# Check storage
curl http://localhost:5000/api/v1/storage-stats

# Manual cleanup
curl -X POST http://localhost:5000/api/v1/cleanup-uploads
```

---

## Project Structure

```
pronuciation_checker/
├── app/
│   ├── AI_module/           # AI workflows and nodes
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic & scheduler
│   └── utils/               # Utilities & cleanup
├── scripts/
│   ├── setup_ec2.sh        # AWS infrastructure setup
│   ├── deploy_app.sh       # Application deployment
│   ├── deploy_docker.sh    # Docker deployment
│   ├── deploy_cloudformation.sh
│   └── cleanup_cron.sh     # Cron job for cleanup
├── cloudformation/
│   └── pronunciation-checker.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── .env                    # Create this from .env.example
```

---

## Common Commands

### Local Development

```bash
# Run application
python run.py

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Docker

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

### EC2 Production

```bash
# View logs
sudo journalctl -u pronunciation-checker -f

# Restart service
sudo systemctl restart pronunciation-checker

# Check status
sudo systemctl status pronunciation-checker

# Update code
cd /home/ubuntu/pronuciation_checker
git pull
sudo systemctl restart pronunciation-checker
```

---

## Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u pronunciation-checker -n 100

# Verify dependencies
source venv/bin/activate
pip list
```

### Port already in use

```bash
# Find process
sudo lsof -i :5000

# Kill process
sudo kill -9 PID
```

### Google API errors

- Verify API key in `.env`
- Check quota in Google Cloud Console
- Ensure Gemini API is enabled

### Out of memory

```bash
# Check memory
free -h

# Add swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Security Best Practices

- ✅ Never commit `.env` file
- ✅ Use strong `SECRET_KEY`
- ✅ Restrict SSH access (security groups)
- ✅ Enable HTTPS with Let's Encrypt
- ✅ Regular updates: `sudo apt update && sudo apt upgrade`
- ✅ Monitor CloudWatch for unusual activity
- ✅ Use IAM roles instead of access keys

---

## Performance

- **Max file size**: 16MB
- **Supported formats**: MP3, WAV, WebM
- **Processing time**: 2-5 seconds (depends on audio length)
- **Concurrent requests**: Handled by Gunicorn workers
- **Memory usage**: ~200-500MB per worker

---

## Cost Estimation

### AWS EC2 t3.small

- Instance: ~$15/month
- Storage (20GB): ~$2/month
- Data transfer: ~$1-5/month
- **Total**: ~$18-22/month

### AWS Free Tier

- t2.micro instance FREE for 12 months
- 30GB storage FREE for 12 months
- Perfect for testing!

---

## Development

### Adding New Endpoints

1. Create route in `app/routes/api.py`
2. Add service logic in `app/services/`
3. Update AI workflows in `app/AI_module/` if needed
4. Test locally
5. Deploy

### Modifying AI Prompts

Edit prompts in `app/AI_module/nodes.py`:
- `analyze_pronunciation_errors_node`
- `evaluate_speech_metrics_node`
- `generate_speaking_report_node`

---

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

## Support

For issues and questions:
- Check logs first
- Review error messages
- Verify environment variables
- Ensure Google API key is valid

---

## Acknowledgments

- Google Gemini AI
- LangChain & LangGraph
- Flask Framework
- AWS

---

**Made with ❤️ for English learners**
