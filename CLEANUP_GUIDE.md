# Automatic Upload Cleanup System

## Overview

The application now includes an automatic cleanup system that deletes old audio files from the `uploads` folder to prevent storage limits. This helps manage disk space and keeps your server running smoothly.

## Features

### 1. **Automatic Background Cleanup**
- Runs automatically in the background
- Configurable retention period (default: 7 days)
- Configurable cleanup interval (default: every 24 hours)
- Logs all cleanup operations

### 2. **Manual Cleanup API**
- Trigger cleanup on-demand via API
- Check storage statistics
- Custom retention period per request

### 3. **Cron Job Backup**
- Optional cron job for redundancy
- Runs independently of the application
- Useful for additional safety

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Enable/disable automatic cleanup
CLEANUP_ENABLED=true

# Maximum age of files before deletion (in days)
CLEANUP_MAX_AGE_DAYS=7

# How often to run cleanup (in hours)
CLEANUP_INTERVAL_HOURS=24
```

### Default Settings

If not configured, the system uses these defaults:
- **Enabled**: `true`
- **Max Age**: `7 days`
- **Interval**: `24 hours` (daily)

## How It Works

### Automatic Cleanup

1. **On Application Start**: Cleanup runs immediately
2. **Scheduled Runs**: Cleanup runs every `CLEANUP_INTERVAL_HOURS`
3. **File Selection**: Files older than `CLEANUP_MAX_AGE_DAYS` are deleted
4. **Logging**: All operations are logged with details

### File Age Calculation

Files are considered "old" based on their **modification time** (`mtime`):
- If a file was last modified more than `CLEANUP_MAX_AGE_DAYS` ago, it will be deleted
- Empty directories are also removed after cleanup

## API Endpoints

### Get Storage Statistics

```bash
GET /api/v1/storage-stats
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_files": 42,
    "total_size_mb": 156.7,
    "oldest_file_age_days": 12.3
  }
}
```

### Manual Cleanup

```bash
POST /api/v1/cleanup-uploads
Content-Type: application/json

{
  "max_age_days": 7
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "deleted_count": 15,
    "freed_space_mb": 45.2,
    "max_age_days": 7,
    "errors": null
  }
}
```

## Cron Job Setup (Optional)

For additional redundancy, you can set up a cron job:

### 1. Make Script Executable

```bash
chmod +x /home/ubuntu/pronuciation_checker/scripts/cleanup_cron.sh
```

### 2. Edit Crontab

```bash
crontab -e
```

### 3. Add Cron Entry

```bash
# Run cleanup daily at 2 AM
0 2 * * * /home/ubuntu/pronuciation_checker/scripts/cleanup_cron.sh

# Or run every 6 hours
0 */6 * * * /home/ubuntu/pronuciation_checker/scripts/cleanup_cron.sh
```

### 4. View Cron Logs

```bash
tail -f /var/log/pronunciation-checker/cleanup.log
```

## Monitoring

### View Application Logs

```bash
# View cleanup logs in application
sudo journalctl -u pronunciation-checker | grep -i cleanup

# Follow logs in real-time
sudo journalctl -u pronunciation-checker -f | grep -i cleanup
```

### Check Storage Usage

```bash
# Check upload folder size
du -sh /home/ubuntu/pronuciation_checker/uploads

# List files by age
find /home/ubuntu/pronuciation_checker/uploads -type f -printf '%T+ %p\n' | sort
```

## Examples

### Example 1: Check Current Storage

```bash
curl http://localhost/api/v1/storage-stats
```

### Example 2: Manual Cleanup (7 days)

```bash
curl -X POST http://localhost/api/v1/cleanup-uploads \
  -H "Content-Type: application/json" \
  -d '{"max_age_days": 7}'
```

### Example 3: Aggressive Cleanup (1 day)

```bash
curl -X POST http://localhost/api/v1/cleanup-uploads \
  -H "Content-Type: application/json" \
  -d '{"max_age_days": 1}'
```

## Customization

### Change Retention Period

Edit `.env`:
```bash
CLEANUP_MAX_AGE_DAYS=14  # Keep files for 14 days
```

Restart application:
```bash
sudo systemctl restart pronunciation-checker
```

### Change Cleanup Frequency

Edit `.env`:
```bash
CLEANUP_INTERVAL_HOURS=12  # Run every 12 hours
```

Restart application:
```bash
sudo systemctl restart pronunciation-checker
```

### Disable Automatic Cleanup

Edit `.env`:
```bash
CLEANUP_ENABLED=false
```

You can still use the manual API endpoint even when automatic cleanup is disabled.

## Troubleshooting

### Cleanup Not Running

1. **Check if enabled**:
   ```bash
   grep CLEANUP_ENABLED /home/ubuntu/pronuciation_checker/.env
   ```

2. **Check logs**:
   ```bash
   sudo journalctl -u pronunciation-checker | grep -i "cleanup scheduler"
   ```

3. **Verify configuration**:
   ```bash
   curl http://localhost/api/v1/storage-stats
   ```

### Files Not Being Deleted

1. **Check file ages**:
   ```bash
   find /home/ubuntu/pronuciation_checker/uploads -type f -mtime +7
   ```

2. **Check permissions**:
   ```bash
   ls -la /home/ubuntu/pronuciation_checker/uploads
   ```

3. **Run manual cleanup**:
   ```bash
   curl -X POST http://localhost/api/v1/cleanup-uploads
   ```

### High Disk Usage

If you're running out of space:

1. **Immediate cleanup** (delete files older than 1 day):
   ```bash
   curl -X POST http://localhost/api/v1/cleanup-uploads \
     -H "Content-Type: application/json" \
     -d '{"max_age_days": 1}'
   ```

2. **Check what's using space**:
   ```bash
   du -sh /home/ubuntu/pronuciation_checker/*
   ```

3. **Manual cleanup** (if API is down):
   ```bash
   bash /home/ubuntu/pronuciation_checker/scripts/cleanup_cron.sh
   ```

## Best Practices

1. **Monitor Storage**: Regularly check storage stats via API
2. **Adjust Retention**: Set `CLEANUP_MAX_AGE_DAYS` based on your needs
3. **Enable Logging**: Keep logs to track cleanup operations
4. **Use Cron Backup**: Set up cron job for redundancy
5. **Test First**: Test cleanup with a longer retention period initially
6. **Monitor Logs**: Watch logs after deployment to ensure cleanup works

## Security Notes

- Cleanup only affects files in the `UPLOAD_FOLDER`
- Files are permanently deleted (not recoverable)
- No external files are touched
- Runs with application user permissions
- Logs all deletion operations

## Performance Impact

- **Minimal CPU usage**: Cleanup runs in background thread
- **Low I/O impact**: Only scans files once per interval
- **No blocking**: Application continues serving requests during cleanup
- **Efficient**: Only processes files older than threshold

## Summary

The automatic cleanup system provides:
- ✅ Automatic background cleanup
- ✅ Configurable retention and frequency
- ✅ Manual cleanup API
- ✅ Storage statistics endpoint
- ✅ Cron job backup option
- ✅ Comprehensive logging
- ✅ Zero-downtime operation

**Default behavior**: Deletes files older than 7 days, runs daily, starts automatically with the application.
