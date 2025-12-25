import threading
import time
import logging
from app.utils.cleanup import FileCleanupService

logger = logging.getLogger(__name__)


class CleanupScheduler:
    """Background scheduler for automatic file cleanup"""
    
    def __init__(self, upload_folder: str, max_age_days: int = 7, interval_hours: int = 24):
        """
        Initialize cleanup scheduler
        
        Args:
            upload_folder: Path to uploads directory
            max_age_days: Maximum age of files before deletion
            interval_hours: How often to run cleanup (in hours)
        """
        self.upload_folder = upload_folder
        self.max_age_days = max_age_days
        self.interval_seconds = interval_hours * 60 * 60
        self.cleanup_service = FileCleanupService(upload_folder, max_age_days)
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the cleanup scheduler in background thread"""
        if self.running:
            logger.warning("Cleanup scheduler is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info(
            f"Cleanup scheduler started: "
            f"max_age={self.max_age_days} days, "
            f"interval={self.interval_seconds / 3600} hours"
        )
    
    def stop(self):
        """Stop the cleanup scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Cleanup scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        # Run cleanup immediately on start
        self._run_cleanup()
        
        # Then run on schedule
        while self.running:
            time.sleep(self.interval_seconds)
            if self.running:  # Check again after sleep
                self._run_cleanup()
    
    def _run_cleanup(self):
        """Execute cleanup operation"""
        try:
            logger.info("Starting scheduled cleanup...")
            result = self.cleanup_service.cleanup_old_files()
            logger.info(
                f"Scheduled cleanup completed: "
                f"{result['deleted_count']} files deleted, "
                f"{result['freed_space_mb']} MB freed"
            )
        except Exception as e:
            logger.error(f"Scheduled cleanup failed: {str(e)}")


# Global scheduler instance
_scheduler = None


def init_scheduler(app):
    """
    Initialize and start the cleanup scheduler
    
    Args:
        app: Flask application instance
    """
    global _scheduler
    
    if not app.config.get('CLEANUP_ENABLED', True):
        logger.info("Cleanup scheduler is disabled")
        return
    
    upload_folder = app.config.get('UPLOAD_FOLDER', './uploads')
    max_age_days = app.config.get('CLEANUP_MAX_AGE_DAYS', 7)
    interval_hours = app.config.get('CLEANUP_INTERVAL_HOURS', 24)
    
    _scheduler = CleanupScheduler(upload_folder, max_age_days, interval_hours)
    _scheduler.start()


def stop_scheduler():
    """Stop the cleanup scheduler"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        _scheduler = None
