#!/bin/bash

echo "🚀 Starting Log Generator with Datadog Integration"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your Datadog API key:"
    echo "cp env.example .env"
    echo "Then edit .env and add your API key"
    exit 1
fi

# Check if API key is set
if grep -q "your_datadog_api_key_here" .env; then
    echo "❌ Please update .env file with your actual Datadog API key"
    exit 1
fi

echo "✅ Environment configured"

# Start Datadog agent
echo "🐕 Starting Datadog agent..."
docker-compose up -d

# Wait for agent to start
echo "⏳ Waiting for Datadog agent to start..."
sleep 10

# Check agent status
echo "🔍 Checking agent status..."
docker exec datadog-agent agent status --json | grep -q "running" && echo "✅ Agent is running" || echo "⚠️  Agent may not be fully started yet"

# Generate logs
echo "📝 Generating logs..."
python log_generator.py

echo "✅ Setup complete!"
echo "📊 View your logs at: https://app.datadoghq.com/logs?query=service:log-generator" 