import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class FileCleanupService:
    """Service to automatically clean up old uploaded files"""
    
    def __init__(self, upload_folder: str, max_age_days: int = 7):
        """
        Initialize cleanup service
        
        Args:
            upload_folder: Path to uploads directory
            max_age_days: Maximum age of files in days before deletion (default: 7)
        """
        self.upload_folder = Path(upload_folder)
        self.max_age_days = max_age_days
        self.max_age_seconds = max_age_days * 24 * 60 * 60
        
    def cleanup_old_files(self) -> dict:
        """
        Remove files older than max_age_days
        
        Returns:
            dict: Statistics about cleanup operation
        """
        if not self.upload_folder.exists():
            logger.warning(f"Upload folder does not exist: {self.upload_folder}")
            return {
                'deleted_count': 0,
                'freed_space_mb': 0,
                'error': 'Upload folder does not exist'
            }
        
        current_time = time.time()
        cutoff_time = current_time - self.max_age_seconds
        
        deleted_count = 0
        freed_space = 0
        errors = []
        
        try:
            # Iterate through all files in upload folder
            for file_path in self.upload_folder.rglob('*'):
                if file_path.is_file():
                    try:
                        # Get file modification time
                        file_mtime = file_path.stat().st_mtime
                        
                        # Check if file is older than cutoff
                        if file_mtime < cutoff_time:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            deleted_count += 1
                            freed_space += file_size
                            
                            logger.info(
                                f"Deleted old file: {file_path.name} "
                                f"(age: {(current_time - file_mtime) / 86400:.1f} days)"
                            )
                    except Exception as e:
                        error_msg = f"Error deleting {file_path.name}: {str(e)}"
                        logger.error(error_msg)
                        errors.append(error_msg)
            
            # Clean up empty directories
            self._cleanup_empty_dirs()
            
            freed_space_mb = freed_space / (1024 * 1024)
            
            logger.info(
                f"Cleanup completed: {deleted_count} files deleted, "
                f"{freed_space_mb:.2f} MB freed"
            )
            
            return {
                'deleted_count': deleted_count,
                'freed_space_mb': round(freed_space_mb, 2),
                'max_age_days': self.max_age_days,
                'errors': errors if errors else None
            }
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return {
                'deleted_count': deleted_count,
                'freed_space_mb': round(freed_space / (1024 * 1024), 2),
                'error': str(e)
            }
    
    def _cleanup_empty_dirs(self):
        """Remove empty subdirectories in upload folder"""
        for dirpath in sorted(self.upload_folder.rglob('*'), reverse=True):
            if dirpath.is_dir() and not any(dirpath.iterdir()):
                try:
                    dirpath.rmdir()
                    logger.info(f"Removed empty directory: {dirpath}")
                except Exception as e:
                    logger.error(f"Error removing directory {dirpath}: {str(e)}")
    
    def get_storage_stats(self) -> dict:
        """
        Get current storage statistics
        
        Returns:
            dict: Storage statistics
        """
        if not self.upload_folder.exists():
            return {
                'total_files': 0,
                'total_size_mb': 0,
                'oldest_file_age_days': 0
            }
        
        total_files = 0
        total_size = 0
        oldest_mtime = time.time()
        current_time = time.time()
        
        for file_path in self.upload_folder.rglob('*'):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size
                file_mtime = file_path.stat().st_mtime
                if file_mtime < oldest_mtime:
                    oldest_mtime = file_mtime
        
        oldest_age_days = (current_time - oldest_mtime) / 86400 if total_files > 0 else 0
        
        return {
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'oldest_file_age_days': round(oldest_age_days, 1)
        }


def cleanup_uploads(upload_folder: str, max_age_days: int = 7) -> dict:
    """
    Convenience function to clean up old uploads
    
    Args:
        upload_folder: Path to uploads directory
        max_age_days: Maximum age of files in days
        
    Returns:
        dict: Cleanup statistics
    """
    service = FileCleanupService(upload_folder, max_age_days)
    return service.cleanup_old_files()
