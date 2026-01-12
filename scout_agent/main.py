"""
Silent Scout - Main Execution Loop
Coordinates hardware initialization, user input detection, and the scanning workflow.
"""

import time
import gc
import scout
from config import configs


# Application configuration mapping
LED_PIN: int = configs["led_pin"]
BTN_PIN: int = configs["btn_pin"]
FILE_NAME: str = configs["archive_file"]

# Hardware Initialization
status_led = scout.init_led(LED_PIN)
trigger_btn = scout.init_btn(BTN_PIN)

print("[SYSTEM] Silent Scout Booted. Operational.")

while True:
    # 1. SAFETY DELAY
    # Prevents accidental double triggers and stabilizes the system
    print("\n[SYSTEM] Entering 2s safety delay...")
    scout.led_off(status_led)
    time.sleep(2)

    # 2. TRIGGER WINDOW (5s)
    # Waiting for user input while providing visual feedback (Breathing LED)
    print("[READY] Waiting for trigger (5s window)...")
    start_time = time.ticks_ms()
    button_pressed: bool = False
    
    while time.ticks_diff(time.ticks_ms(), start_time) < 5000:
        if trigger_btn.value() == 0:  # Button Detection (Active Low)
            button_pressed = True
            break
        
        # Dynamic Breathing Effect (Pulse) - 1 cycle per second
        elapsed_ms = time.ticks_diff(time.ticks_ms(), start_time)
        cycle_ms = elapsed_ms % 1000
        
        if cycle_ms < 500:
            # Fade In: 0-100%
            brightness = (cycle_ms / 500) * 100
        else:
            # Fade Out: 100-0%
            brightness = (1000 - cycle_ms) / 500 * 100
        
        scout.led_set_brightness(status_led, brightness)
        time.sleep_ms(10)

    # 3. ACTION SEQUENCE
    if button_pressed:
        scout.led_on(status_led)  # Maximum brightness during operation
        
        print("[SYSTEM] Performing pre-scan memory optimization...")
        gc.collect()
        
        print("[ACTION] Starting WiFi reconnaissance...")
        scan_results = scout.do_triscan()
        network_count = len(scan_results)
        print(f"[SCOUT] Scan complete. {network_count} networks identified.")
        
        print("[SAVE] Committing results to data vault...")
        locality_id = scout.get_next_id()
        scout.save_to_csv(FILE_NAME, scan_results, locality_id)
        
        print("[DONE] Data successfully saved into the file.")
        
        scout.led_off(status_led)
        time.sleep(1)
        
        # Visual success confirmation
        scout.signal_success(status_led)
        
        # Cleanup and memory release
        scan_results = None
        gc.collect()
        print("[SYSTEM] Memory optimized after scan cycle.")
    else:
        print("[TIMEOUT] No trigger detected. Restarting loop.")
        scout.led_off(status_led)

    # Return to safety delay (Automatic loop restart)