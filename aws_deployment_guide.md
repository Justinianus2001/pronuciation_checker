# AWS Deployment Guide for Pronunciation Checker

## Application Overview

This is a Flask-based pronunciation checker application that uses Google's Gemini AI to:
- Analyze pronunciation errors in audio recordings
- Evaluate speech metrics based on IELTS criteria
- Generate speaking performance reports

### Technology Stack
- **Backend**: Flask (Python)
- **AI/ML**: LangChain, LangGraph, Google Gemini 2.0 Flash
- **Dependencies**: See `requirements.txt`

### API Endpoints
- `POST /api/v1/analyze-pronunciation-error` - Analyze pronunciation errors
- `POST /api/v1/evaluate-speech-metrics` - Evaluate IELTS speaking metrics
- `POST /api/v1/generate-speaking-report` - Generate comprehensive report
- `GET /api/v1/health-check` - Health check endpoint

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Google API Key** for Gemini AI
3. **AWS CLI** installed and configured
4. **SSH Key Pair** for EC2 access

## Deployment Options

### Option 1: EC2 Deployment (Recommended for getting started)
- Simple setup
- Full control over the server
- Cost-effective for low to medium traffic

### Option 2: Elastic Beanstalk (Recommended for production)
- Managed service
- Auto-scaling
- Load balancing
- Easy deployment and updates

### Option 3: ECS with Fargate (Containerized)
- Serverless containers
- Highly scalable
- No server management

## Quick Start - EC2 Deployment

### Step 1: Launch EC2 Instance

```bash
# Run the EC2 setup script
bash scripts/setup_ec2.sh
```

### Step 2: Deploy Application

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Run the deployment script
bash deploy_app.sh
```

### Step 3: Configure Environment

```bash
# Edit the .env file with your Google API key
nano /home/ubuntu/pronuciation_checker/.env
```

### Step 4: Start Application

```bash
# Start the application using systemd
sudo systemctl start pronunciation-checker
sudo systemctl enable pronunciation-checker
```

## Environment Variables

Required environment variables:
- `GOOGLE_API_KEY` - Your Google Gemini API key (required)
- `SECRET_KEY` - Flask secret key (optional, auto-generated if not set)
- `UPLOAD_FOLDER` - Upload directory (default: ./uploads)

## Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **Security Groups**: Restrict access to necessary ports only
3. **HTTPS**: Use SSL/TLS certificates (Let's Encrypt recommended)
4. **IAM Roles**: Use IAM roles instead of access keys when possible
5. **Updates**: Regularly update system packages and dependencies

## Monitoring and Logging

- Application logs: `/var/log/pronunciation-checker/`
- System logs: `journalctl -u pronunciation-checker`
- AWS CloudWatch integration available

## Scaling Considerations

- **Vertical Scaling**: Upgrade EC2 instance type for more resources
- **Horizontal Scaling**: Use Application Load Balancer + Auto Scaling Group
- **Caching**: Consider Redis for session management
- **CDN**: Use CloudFront for static assets

## Cost Estimation

**EC2 t3.small (Recommended minimum)**
- Instance: ~$15/month
- Storage (20GB): ~$2/month
- Data transfer: Variable
- **Total**: ~$17-30/month

**Elastic Beanstalk**
- Similar to EC2 + small management fee
- **Total**: ~$20-35/month

## Troubleshooting

### Application won't start
```bash
# Check logs
sudo journalctl -u pronunciation-checker -n 50

# Check if port is in use
sudo netstat -tulpn | grep 5000
```

### Permission issues
```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /home/ubuntu/pronuciation_checker
```

### Out of memory
```bash
# Check memory usage
free -h

# Consider upgrading instance type or adding swap
```

## Support and Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Google Gemini API](https://ai.google.dev/docs)
