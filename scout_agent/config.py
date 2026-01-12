# Global configuration dictionary
# Type hint: dict[str, any] - using any for mixed types (str and int)

configs: dict = {
    "data_dir": "/data",                # Root directory for storage
    "archive_file": "/data/vault.csv",  # Full path to the data vault
    "led_pin": 2,                       # GPIO pin for the status LED
    "btn_pin": 0                        # GPIO pin for the trigger button
}