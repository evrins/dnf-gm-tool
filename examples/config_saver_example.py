"""
Example demonstrating the use of ConfigSaverWorker for async config saving.

This example shows how the config saver worker thread prevents UI blocking
when saving configuration files.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from config import config


class ConfigSaverDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Config Saver Worker Demo")
        self.resize(400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add label
        self.label = QLabel("Click the button to save config asynchronously")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        # Add save button
        save_btn = QPushButton("Save Config (Async)")
        save_btn.clicked.connect(self.save_config_async)
        layout.addWidget(save_btn)
        
        # Add sync save button for comparison
        sync_save_btn = QPushButton("Save Config (Sync - Blocks UI)")
        sync_save_btn.clicked.connect(self.save_config_sync)
        layout.addWidget(sync_save_btn)
        
        # Add status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.save_count = 0
    
    def save_config_async(self):
        """Save config using async worker thread (non-blocking)"""
        self.save_count += 1
        self.status_label.setText(f"Saving config asynchronously... (count: {self.save_count})")
        
        # This uses the worker thread and doesn't block the UI
        config.save()
        
        # UI remains responsive immediately
        self.status_label.setText(f"Save initiated (async) - UI still responsive! (count: {self.save_count})")
    
    def save_config_sync(self):
        """Save config synchronously (blocking)"""
        self.save_count += 1
        self.status_label.setText(f"Saving config synchronously... (count: {self.save_count})")
        
        # This blocks the UI thread
        config.save_sync()
        
        # UI is blocked until save completes
        self.status_label.setText(f"Save completed (sync) - UI was blocked (count: {self.save_count})")


def main():
    # Initialize config
    config.init_dirs()
    config.load()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show demo window
    demo = ConfigSaverDemo()
    demo.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
