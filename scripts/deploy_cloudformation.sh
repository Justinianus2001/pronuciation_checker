#!/bin/bash

###############################################################################
# CloudFormation Deployment Script
# This script deploys the application using AWS CloudFormation
###############################################################################

set -e

STACK_NAME="pronunciation-checker"
TEMPLATE_FILE="cloudformation/pronunciation-checker.yaml"
REGION="us-east-1"

echo "=========================================="
echo "CloudFormation Deployment"
echo "=========================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed."
    exit 1
fi

# Prompt for parameters
read -p "Enter your EC2 Key Pair name: " KEY_NAME
read -sp "Enter your Google API Key: " GOOGLE_API_KEY
echo ""
read -p "Enter instance type (default: t3.small): " INSTANCE_TYPE
INSTANCE_TYPE=${INSTANCE_TYPE:-t3.small}

read -p "Enter SSH access CIDR (default: 0.0.0.0/0): " SSH_CIDR
SSH_CIDR=${SSH_CIDR:-0.0.0.0/0}

# Deploy stack
echo "Deploying CloudFormation stack..."
aws cloudformation create-stack \
    --stack-name "$STACK_NAME" \
    --template-body "file://$TEMPLATE_FILE" \
    --parameters \
        ParameterKey=KeyName,ParameterValue="$KEY_NAME" \
        ParameterKey=GoogleApiKey,ParameterValue="$GOOGLE_API_KEY" \
        ParameterKey=InstanceType,ParameterValue="$INSTANCE_TYPE" \
        ParameterKey=SSHLocation,ParameterValue="$SSH_CIDR" \
    --region "$REGION"

echo "Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete \
    --stack-name "$STACK_NAME" \
    --region "$REGION"

# Get outputs
echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

echo ""
echo "To delete the stack:"
echo "  aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION"
