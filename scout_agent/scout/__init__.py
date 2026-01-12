"""
Silent Scout - Core Package
Provides a unified interface for scanning logic and hardware control.
"""

# Exposing logic functions
from .logic import (
    do_triscan, 
    save_to_csv, 
    get_next_id, 
    delete_vault, 
    reset_locality_id,
    ensure_data_dir
)

# Exposing hardware functions
from .hardware import (
    init_led, 
    init_btn, 
    led_off, 
    led_on, 
    led_set_brightness, 
    signal_success
)