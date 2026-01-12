import time
import scout
from config import configs


# Configuration mapping from central config
TARGET_VAULT: str = configs["archive_file"]
LED_PIN: int = configs["led_pin"]

def run_cleanup() -> None:
    """
    Performs a complete system maintenance by clearing collected data and resetting counters.
    
    The maintenance sequence includes:
    1. Initializing hardware indicators.
    2. Deleting the local CSV data vault.
    3. Resetting the Locality ID in Non-Volatile Storage (NVS).
    4. Providing visual feedback upon completion.
    """
    print("[MAINTENANCE] Initializing full system cleanup...")
    
    # 1. Initialize hardware for signaling
    led = scout.init_led(LED_PIN)
    
    # 2. Delete the data file
    scout.delete_vault(TARGET_VAULT)
    print("[SYSTEM] Data file removed.")
    
    # 3. Reset the Locality ID counter in NVS
    scout.reset_locality_id()
    print("[SYSTEM] Deployment ready. Next Locality ID will be: 1")
    print("[MAINTENANCE] Cleanup finished successfully.")
    
    # 4. Visual confirmation signal (Fast blinking sequence)
    scout.signal_success(led)
    

if __name__ == "__main__":
    try:
        run_cleanup()
    except Exception as e:
        print(f"[ERROR] Maintenance failed: {e}")