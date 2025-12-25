# Quick Start Guide - AWS Deployment

## 📋 Application Summary

**Pronunciation Checker** is a Flask-based AI application that analyzes English pronunciation using Google's Gemini AI.

### Features
- Pronunciation error detection
- IELTS speaking metrics evaluation
- Comprehensive speaking reports
- Audio file processing (MP3, WAV, WebM)
- **Automatic cleanup** of old uploads (prevents storage issues)

### Tech Stack
- **Backend**: Flask + Python 3.11
- **AI**: Google Gemini 2.0 Flash via LangChain
- **Server**: Gunicorn + Nginx

---

## 🚀 Deployment Options

### Option 1: EC2 (Recommended for Beginners)
**Best for**: Simple setup, full control, learning AWS

```bash
# 1. Setup AWS infrastructure
cd scripts
bash setup_ec2.sh

# 2. SSH into instance (wait 2-3 minutes after creation)
ssh -i pronunciation-checker-key.pem ubuntu@YOUR_IP

# 3. Upload your code to the instance
# (Use git clone or scp to transfer files)

# 4. Run deployment script
bash scripts/deploy_app.sh

# 5. Configure your Google API key
nano /home/ubuntu/pronuciation_checker/.env
# Add: GOOGLE_API_KEY=your_actual_key

# 6. Restart service
sudo systemctl restart pronunciation-checker

# 7. Test
curl http://YOUR_IP/api/v1/health-check
```

### Option 2: Docker (Recommended for Consistency)
**Best for**: Consistent environments, easy scaling

```bash
# 1. Install Docker on your server/local machine
# 2. Configure environment
cp .env.example .env
nano .env  # Add your GOOGLE_API_KEY

# 3. Deploy
bash scripts/deploy_docker.sh

# 4. Access application
curl http://localhost/api/v1/health-check
```

### Option 3: CloudFormation (Infrastructure as Code)
**Best for**: Repeatable deployments, team environments

```bash
# 1. Deploy stack
aws cloudformation create-stack \
  --stack-name pronunciation-checker \
  --template-body file://cloudformation/pronunciation-checker.yaml \
  --parameters \
    ParameterKey=KeyName,ParameterValue=your-key-name \
    ParameterKey=GoogleApiKey,ParameterValue=your-api-key

# 2. Wait for completion
aws cloudformation wait stack-create-complete \
  --stack-name pronunciation-checker

# 3. Get outputs
aws cloudformation describe-stacks \
  --stack-name pronunciation-checker \
  --query 'Stacks[0].Outputs'
```

---

## 🔑 Prerequisites

### Required
1. **Google API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **AWS Account** - [Sign up](https://aws.amazon.com/)

### For EC2/CloudFormation
3. **AWS CLI** - [Install guide](https://aws.amazon.com/cli/)
4. **SSH Key Pair** - Created automatically by setup script

### For Docker
3. **Docker** - [Install guide](https://docs.docker.com/get-docker/)
4. **Docker Compose** - Usually included with Docker Desktop

---

## 📝 Environment Variables

Create a `.env` file with:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (auto-generated if not set)
SECRET_KEY=your-secret-key
UPLOAD_FOLDER=./uploads

# Cleanup (optional - defaults shown)
CLEANUP_ENABLED=true
CLEANUP_MAX_AGE_DAYS=7
CLEANUP_INTERVAL_HOURS=24
```

---

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl http://YOUR_IP/api/v1/health-check
# Expected: {"status":"ok"}
```

### 2. Test Pronunciation Analysis
```bash
curl -X POST http://YOUR_IP/api/v1/analyze-pronunciation-error \
  -F "audio=@test_audio.mp3" \
  -F "text=Hello world"
```

### 3. Test Speech Metrics
```bash
curl -X POST http://YOUR_IP/api/v1/evaluate-speech-metrics \
  -F "audio=@test_audio.mp3" \
  -F "text=Hello world"
```

---

## 🛠️ Common Commands

### EC2 Deployment
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

### Docker Deployment
```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## 💰 Cost Estimate

### EC2 t3.small (Recommended)
- **Instance**: ~$15/month
- **Storage**: ~$2/month (20GB)
- **Data Transfer**: ~$1-5/month
- **Total**: ~$18-22/month

### Docker on EC2 t3.small
- Same as above

### CloudFormation with Elastic IP
- Same as EC2 + $3.60/month for Elastic IP
- **Total**: ~$21-26/month

> 💡 **Tip**: Use AWS Free Tier (t2.micro) for first 12 months - FREE!

---

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Never commit .env file
- [ ] Restrict SSH access (update security group)
- [ ] Enable HTTPS with Let's Encrypt
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade`
- [ ] Monitor AWS CloudWatch for unusual activity
- [ ] Use IAM roles instead of access keys
- [ ] Enable AWS CloudTrail for audit logs

---

## 🐛 Troubleshooting

### Application won't start
```bash
# Check logs
sudo journalctl -u pronunciation-checker -n 100

# Verify Python dependencies
source /home/ubuntu/pronuciation_checker/venv/bin/activate
pip list
```

### Port already in use
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill if needed
sudo kill -9 PID
```

### Out of memory
```bash
# Check memory
free -h

# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Google API errors
- Verify API key is correct in `.env`
- Check API quota in Google Cloud Console
- Ensure Gemini API is enabled

---

## 📚 Additional Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Docker Documentation](https://docs.docker.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

## 🆘 Getting Help

1. Check logs first (see Common Commands)
2. Review error messages carefully
3. Verify all environment variables are set
4. Ensure Google API key is valid
5. Check AWS service health dashboard

---

## 📄 File Structure

```
pronuciation_checker/
├── app/                          # Application code
│   ├── AI_module/               # AI workflows
│   ├── routes/                  # API endpoints
│   ├── services/                # Business logic
│   └── utils/                   # Utilities
├── scripts/                     # Deployment scripts
│   ├── setup_ec2.sh            # EC2 infrastructure
│   ├── deploy_app.sh           # App deployment
│   └── deploy_docker.sh        # Docker deployment
├── cloudformation/              # CloudFormation templates
├── Dockerfile                   # Docker image
├── docker-compose.yml          # Docker orchestration
├── nginx.conf                  # Nginx config
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── .env                        # Environment variables (create this)
```

---

**Ready to deploy? Start with Option 1 (EC2) for the simplest path!** 🎉
