#!/bin/bash

set -e

# Configuration
BACKUP_DIR="/backups/phishshield"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "💾 Starting backup process..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
echo "📦 Backing up database..."
docker-compose -f docker-compose.production.yml exec -T db pg_dump -U phishshield_user phishshield > $BACKUP_DIR/db_backup_$DATE.sql

# Backup logs
echo "📋 Backing up logs..."
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /var/log/phishshield/ 2>/dev/null || true

# Backup media files (if any)
if [ -d "media" ]; then
    echo "🖼️ Backing up media files..."
    tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/
fi

# Create backup manifest
cat > $BACKUP_DIR/backup_manifest_$DATE.txt << MANIFEST
Backup created: $(date)
Database: db_backup_$DATE.sql
Logs: logs_backup_$DATE.tar.gz
Media: media_backup_$DATE.tar.gz
MANIFEST

# Clean up old backups
echo "🧹 Cleaning up old backups..."
find $BACKUP_DIR -name "*.sql" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.txt" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup completed: $BACKUP_DIR/backup_manifest_$DATE.txt"

# Optional: Upload to cloud storage
# echo "☁️ Uploading to cloud storage..."
# aws s3 sync $BACKUP_DIR s3://your-backup-bucket/phishshield/ --delete
