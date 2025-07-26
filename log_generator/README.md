# Log Generator with Datadog Integration

This project generates structured logs and sends them to Datadog using a local Docker agent.

## Setup

### 1. Get Datadog API Key
1. Go to [Datadog API Settings](https://app.datadoghq.com/account/settings#api)
2. Copy your API key
3. Create a `.env` file:
```bash
cp env.example .env
```
4. Edit `.env` and replace `your_datadog_api_key_here` with your actual API key

### 2. Start Datadog Agent
```bash
docker-compose up -d
```

### 3. Generate Logs
```bash
python log_generator.py
```

## Files

- `log_generator.py` - Enhanced log generator with structured logging
- `docker-compose.yml` - Datadog agent container setup
- `datadog-agent.yaml` - Agent configuration for log collection
- `custom.log` - Generated log file (auto-created)

## Log Format

Logs are written in CSV format:
```
timestamp,"message",logStreamName
```

Example:
```
1753566348471,"User login succeeded: {"user":"alice","status":"success","timestamp":"2024-01-01T12:00:00"}",service-logs/app-container/instance-001
```

## Datadog Integration

The Datadog agent will:
- Monitor the `custom.log` file
- Parse CSV format logs
- Send structured data to Datadog
- Apply log processing rules for better parsing

## Viewing Logs in Datadog

1. Go to [Datadog Logs](https://app.datadoghq.com/logs)
2. Filter by `service:log-generator`
3. Search for your log entries

## Troubleshooting

Check agent status:
```bash
docker-compose logs datadog-agent
```

Test agent health:
```bash
docker exec datadog-agent agent status
```

## Stopping

```bash
docker-compose down
```
