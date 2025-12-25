#!/bin/bash

###############################################################################
# Cron Job Script for Upload Cleanup
# This script can be run as a cron job for additional cleanup redundancy
###############################################################################

# Configuration
APP_DIR="/home/ubuntu/pronuciation_checker"
UPLOAD_DIR="$APP_DIR/uploads"
MAX_AGE_DAYS=7
LOG_FILE="/var/log/pronunciation-checker/cleanup.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting upload cleanup..."

# Check if upload directory exists
if [ ! -d "$UPLOAD_DIR" ]; then
    log "Upload directory does not exist: $UPLOAD_DIR"
    exit 1
fi

# Count files before cleanup
BEFORE_COUNT=$(find "$UPLOAD_DIR" -type f | wc -l)
BEFORE_SIZE=$(du -sm "$UPLOAD_DIR" 2>/dev/null | cut -f1)

log "Before cleanup: $BEFORE_COUNT files, ${BEFORE_SIZE}MB"

# Delete files older than MAX_AGE_DAYS
DELETED_COUNT=$(find "$UPLOAD_DIR" -type f -mtime +$MAX_AGE_DAYS -delete -print | wc -l)

# Remove empty directories
find "$UPLOAD_DIR" -type d -empty -delete 2>/dev/null

# Count files after cleanup
AFTER_COUNT=$(find "$UPLOAD_DIR" -type f | wc -l)
AFTER_SIZE=$(du -sm "$UPLOAD_DIR" 2>/dev/null | cut -f1)
FREED_SIZE=$((BEFORE_SIZE - AFTER_SIZE))

log "After cleanup: $AFTER_COUNT files, ${AFTER_SIZE}MB"
log "Deleted: $DELETED_COUNT files, freed ${FREED_SIZE}MB"
log "Cleanup completed successfully"

exit 0
