# Config Saver Worker Thread

## Overview

The Config Saver Worker Thread provides asynchronous configuration file saving to prevent blocking the UI thread during I/O operations. This is especially important for maintaining a responsive user interface in GUI applications.

## Features

- **Asynchronous Saving**: Config files are saved in a background thread
- **Non-Blocking UI**: The main UI thread remains responsive during save operations
- **Automatic Queuing**: Multiple save requests are queued and processed sequentially
- **Error Handling**: Graceful error handling with logging
- **Thread Safety**: Proper synchronization to prevent race conditions

## Architecture

### Components

1. **ConfigSaverWorker**: QThread subclass that performs the actual file I/O
2. **ConfigSaverManager**: Manages worker threads and handles queuing
3. **Integration**: Seamlessly integrated into the existing config module

### Flow Diagram

```
User Action → config.save() → ConfigSaverManager → ConfigSaverWorker → File System
                                      ↓
                                  Queue if busy
                                      ↓
                              Process when ready
```

## Usage

### Basic Usage

```python
from config import config

# Initialize config
config.load()

# Save asynchronously (non-blocking)
config.save()  # Returns immediately, save happens in background

# UI remains responsive!
```

### Synchronous Save (When Needed)

```python
from config import config

# Save synchronously (blocking) - use only when necessary
config.save_sync()  # Blocks until save completes
```

### Advanced Usage

```python
from config.config_saver import get_config_saver_manager

# Get the manager instance
manager = get_config_saver_manager()

# Save custom config
manager.save_config_async(
    config_path=Path("custom_config.json"),
    config_json='{"key": "value"}'
)

# Wait for completion if needed
manager.wait_for_completion(timeout_ms=5000)
```

## Implementation Details

### ConfigSaverWorker

```python
class ConfigSaverWorker(QThread):
    save_completed = Signal()
    save_failed = Signal(str)
    
    def run(self):
        # Performs file I/O in background thread
        # Emits signals on completion/failure
```

### ConfigSaverManager

```python
class ConfigSaverManager:
    def save_config_async(self, config_path, config_json):
        # Manages worker threads
        # Queues saves if worker is busy
        # Ensures sequential processing
```

## Benefits

### Performance

- **No UI Freezing**: File I/O doesn't block the main thread
- **Better UX**: Users can continue working while saves happen
- **Efficient**: Queuing prevents multiple simultaneous writes

### Reliability

- **Error Handling**: Failures are logged and don't crash the app
- **Thread Safety**: Proper synchronization prevents corruption
- **Graceful Degradation**: Falls back to sync save if needed

## Testing

Comprehensive tests are provided in `tests/config/test_config_saver.py`:

```bash
# Run tests
python tests/config/test_config_saver.py
```

Tests cover:
- Basic worker functionality
- Manager queuing behavior
- Error handling
- Thread safety

## Example

See `examples/config_saver_example.py` for a complete working example demonstrating:
- Async vs sync saving
- UI responsiveness comparison
- Integration with PySide6

## Migration Guide

### Before (Blocking)

```python
def save():
    with open(config_path, 'w') as f:
        f.write(config_json)  # Blocks UI thread
```

### After (Non-Blocking)

```python
def save():
    from config.config_saver import get_config_saver_manager
    
    saver = get_config_saver_manager()
    saver.save_config_async(config_path, config_json)  # Returns immediately
```

## Best Practices

1. **Use Async by Default**: Always use `config.save()` (async) unless you have a specific reason to block
2. **Sync Only When Necessary**: Use `config.save_sync()` only for critical operations that must complete before proceeding
3. **Wait on Shutdown**: Call `manager.wait_for_completion()` before application exit to ensure saves complete
4. **Error Monitoring**: Monitor logs for save failures

## Troubleshooting

### Save Not Completing

```python
# Wait for save to complete
from config.config_saver import get_config_saver_manager

manager = get_config_saver_manager()
success = manager.wait_for_completion(timeout_ms=5000)
if not success:
    print("Save timed out!")
```

### Checking Save Status

```python
# Check if a save is in progress
if manager._current_worker and manager._current_worker.isRunning():
    print("Save in progress...")
```

## Future Enhancements

Potential improvements:
- Debouncing for rapid save requests
- Batch saving for multiple configs
- Progress reporting for large files
- Retry logic for transient failures

## See Also

- `config/config.py` - Main configuration module
- `config/config_saver.py` - Worker thread implementation
- `tests/config/test_config_saver.py` - Test suite
- `examples/config_saver_example.py` - Usage example
