import network
import time
import esp32
import gc
import os
from config import configs


def ensure_data_dir() -> None:
    """
    Verifies the existence of the data directory and creates it if necessary.
    """
    data_dir: str = configs["data_dir"]
    try:
        os.stat(data_dir)
    except OSError:
        try:
            os.mkdir(data_dir)
            print(f"[*] Created missing data directory: {data_dir}")
        except OSError as e:
            print(f"[!] Critical error creating directory: {e}")

def get_next_id() -> int:
    """
    Retrieves and increments the Locality ID from Non-Volatile Storage (NVS).
    
    Returns:
        int: The newly assigned Locality ID.
    """
    nvs = esp32.NVS("scout")
    try:
        locality_id = nvs.get_i32("id_loc")
    except OSError:
        locality_id = 0
    
    locality_id += 1
    nvs.set_i32("id_loc", locality_id)
    nvs.commit()
    return locality_id

def do_triscan() -> list:
    """
    Performs a triple WiFi scan sequence and merges unique access points by BSSID.
    Memory is cleared before and after scanning to ensure stability.
    
    Returns:
        list: A consolidated list of unique network scan tuples.
    """
    gc.collect() # Pre-scan memory cleanup
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    scan_results = {}

    for cycle in range(3):
        print(f"[SCAN] Cycle {cycle + 1}/3 in progress...")
        try:
            current_batch = wlan.scan()
            for ap in current_batch:
                # Map BSSID as unique key for merging (Index 1 in tuple)
                bssid = ":".join("%02x" % b for b in ap[1])
                scan_results[bssid] = ap
        except Exception as e:
            print(f"[!] Scan cycle failed: {e}")
            
        time.sleep_ms(300)
    
    wlan.active(False) # Power saving
    gc.collect() # Post-scan memory cleanup
    return list(scan_results.values())

def save_to_csv(filename: str, results: list, locality_id: int) -> None:
    """
    Appends scan results to a CSV file with technical metadata.
    Includes robust SSID decoding and periodic memory management.
    
    Format: ID_LOCALITY;SSID;MAC / BSSID;RSSI;CHANNEL;HIDDEN;SECURITY
    """
    ensure_data_dir()
    
    header_needed = False
    try:
        os.stat(filename)
    except OSError:
        header_needed = True

    try:
        with open(filename, "a") as f:
            if header_needed:
                f.write("ID_LOCALITY;SSID;MAC / BSSID;RSSI;CHANNEL;HIDDEN;SECURITY\n")
            
            for ap in results:
                # Safe SSID decoding: Handle special characters and potential failures
                try:
                    # 'ignore' ensures that non-UTF-8 characters don't crash the script
                    ssid = ap[0].decode('utf-8', 'ignore').replace('"', '')
                except Exception:
                    ssid = "Decoding_Error"
                    
                bssid = ":".join("%02x" % b for b in ap[1])
                channel = ap[2]
                rssi = ap[3]
                security = ap[4]
                hidden = 1 if ap[5] else 0
                
                # Write entry to the data vault
                f.write(f"{locality_id};\"{ssid}\";{bssid};{rssi};{channel};{hidden};{security}\n")
    except Exception as e:
        print(f"[!] Error writing to vault: {e}")
    finally:
        gc.collect() # Ensure buffers and temporary strings are cleared

def delete_vault(filename: str) -> None:
    """
    Permanently removes the data vault file from storage.
    """
    try:
        os.remove(filename)
        print(f"[CLEAN] Vault file '{filename}' has been purged.")
    except OSError:
        print(f"[!] Purge failed: File '{filename}' not found.")

def reset_locality_id() -> None:
    """
    Resets the operational Locality ID counter in NVS to zero.
    """
    nvs = esp32.NVS("scout")
    nvs.set_i32("id_loc", 0)
    nvs.commit()
    print("[CLEAN] Locality ID counter has been reset.")