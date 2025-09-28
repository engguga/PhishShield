#!/bin/bash

set -e

echo "🏥 Running health checks..."

# Check if containers are running
if ! docker-compose -f docker-compose.production.yml ps | grep -q "Up"; then
    echo "❌ Some containers are not running"
    exit 1
fi

# Check database connection
echo "�� Checking database connection..."
docker-compose -f docker-compose.production.yml exec -T db pg_isready -U phishshield_user

# Check Redis connection
echo "🔍 Checking Redis connection..."
docker-compose -f docker-compose.production.yml exec -T redis redis-cli ping

# Check Django application
echo "🔍 Checking Django application..."
curl -f https://yourdomain.com/health/ > /dev/null 2>&1 || curl -f https://yourdomain.com/admin/ > /dev/null 2>&1

# Check Celery workers
echo "🔍 Checking Celery workers..."
docker-compose -f docker-compose.production.yml exec -T web celery -A core inspect ping

# Check disk space
echo "🔍 Checking disk space..."
df -h | grep -E "(/|/app)" | awk '{print $5 " used on " $1}'

# Check memory usage
echo "🔍 Checking memory usage..."
free -h

echo "✅ All health checks passed!"
