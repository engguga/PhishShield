#!/bin/bash

set -e

echo "🚀 Starting PhishShield deployment..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "❌ .env.production file not found"
    exit 1
fi

# Validate required environment variables
required_vars=("SECRET_KEY" "DATABASE_PASSWORD" "EMAIL_HOST" "EMAIL_HOST_USER" "EMAIL_HOST_PASSWORD")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

# Generate secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
    echo "🔑 Generated new SECRET_KEY"
fi

# Create necessary directories
mkdir -p ssl staticfiles media logs

# Build and start services
echo "📦 Building Docker images..."
docker-compose -f docker-compose.production.yml build

echo "🔄 Starting services..."
docker-compose -f docker-compose.production.yml up -d

echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "🗃️ Running database migrations..."
docker-compose -f docker-compose.production.yml exec web python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput

# Create superuser if not exists
echo "👤 Creating superuser..."
docker-compose -f docker-compose.production.yml exec web python manage.py create_api_user

# Load sample templates
echo "📝 Loading sample templates..."
docker-compose -f docker-compose.production.yml exec web python manage.py load_sample_templates

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Access your application:"
echo "   - Main site: https://yourdomain.com"
echo "   - Admin: https://yourdomain.com/admin"
echo "   - API Docs: https://yourdomain.com/api/docs"
echo ""
echo "🔐 API Credentials:"
echo "   - Username: api_user"
echo "   - Password: SecureAPIpass123!"
echo ""
echo "📋 Next steps:"
echo "   1. Update SSL certificates in ssl/ directory"
echo "   2. Configure your domain DNS"
echo "   3. Set up monitoring and backups"
