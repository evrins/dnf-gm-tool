"""
Config Saver Worker Thread

This module provides a worker thread for saving configuration files
asynchronously to prevent blocking the UI thread.
"""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal
from loguru import logger


class ConfigSaverWorker(QThread):
    """
    Worker thread for saving configuration files asynchronously.
    
    Signals:
        save_completed: Emitted when save operation completes successfully
        save_failed: Emitted when save operation fails (with error message)
    """
    
    save_completed = Signal()
    save_failed = Signal(str)
    
    def __init__(self, config_path: Path, config_json: str):
        """
        Initialize the config saver worker.
        
        Args:
            config_path: Path to the config file
            config_json: JSON string to save
        """
        super().__init__()
        self.config_path = config_path
        self.config_json = config_json
        self._is_running = False
    
    def run(self):
        """Execute the save operation in the worker thread."""
        self._is_running = True
        try:
            logger.debug(f"Saving config to {self.config_path}")
            
            # Ensure parent directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write config to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.write(self.config_json)
            
            logger.info(f"Config saved successfully to {self.config_path}")
            self.save_completed.emit()
            
        except Exception as e:
            error_msg = f"Failed to save config: {e}"
            logger.error(error_msg)
            self.save_failed.emit(error_msg)
            
        finally:
            self._is_running = False
    
    def is_running(self) -> bool:
        """Check if the worker is currently running."""
        return self._is_running


class ConfigSaverManager:
    """
    Manager for config saver worker threads.
    Ensures only one save operation runs at a time.
    """
    
    def __init__(self):
        self._current_worker: Optional[ConfigSaverWorker] = None
        self._pending_save: Optional[tuple[Path, str]] = None
    
    def save_config_async(self, config_path: Path, config_json: str):
        """
        Save config asynchronously using a worker thread.
        
        Args:
            config_path: Path to the config file
            config_json: JSON string to save
        """
        # If a worker is currently running, queue this save
        if self._current_worker and self._current_worker.isRunning():
            logger.debug("Config save already in progress, queuing new save")
            self._pending_save = (config_path, config_json)
            return
        
        # Create and start new worker
        self._start_worker(config_path, config_json)
    
    def _start_worker(self, config_path: Path, config_json: str):
        """Start a new worker thread for saving config."""
        self._current_worker = ConfigSaverWorker(config_path, config_json)
        self._current_worker.save_completed.connect(self._on_save_completed)
        self._current_worker.save_failed.connect(self._on_save_failed)
        self._current_worker.start()
    
    def _on_save_completed(self):
        """Handle successful save completion."""
        logger.debug("Config save completed")
        
        # Clean up current worker
        self._current_worker = None
        
        # If there's a pending save, start it
        if self._pending_save:
            config_path, config_json = self._pending_save
            self._pending_save = None
            logger.debug("Starting queued config save")
            self._start_worker(config_path, config_json)
    
    def _on_save_failed(self, error_msg: str):
        """Handle save failure."""
        logger.error(f"Config save failed: {error_msg}")
        
        # Clean up current worker
        self._current_worker = None
        
        # If there's a pending save, start it anyway
        if self._pending_save:
            config_path, config_json = self._pending_save
            self._pending_save = None
            logger.debug("Starting queued config save after failure")
            self._start_worker(config_path, config_json)
    
    def wait_for_completion(self, timeout_ms: int = 5000) -> bool:
        """
        Wait for current save operation to complete.
        
        Args:
            timeout_ms: Maximum time to wait in milliseconds
            
        Returns:
            True if completed successfully, False if timeout
        """
        if self._current_worker and self._current_worker.isRunning():
            return self._current_worker.wait(timeout_ms)
        return True


# Global instance
_config_saver_manager = ConfigSaverManager()


def get_config_saver_manager() -> ConfigSaverManager:
    """Get the global config saver manager instance."""
    return _config_saver_manager
