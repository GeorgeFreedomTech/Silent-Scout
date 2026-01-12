"""
Silent Scout HQ - Data Ingestion Engine
Handles the transfer of raw CSV data from the Agent into the HQ SQLite database.
"""

import csv
from datetime import datetime
from typing import List, Tuple, Optional
from modules import init_db, save_to_db
from config import SOURCE_CSV


def run_ingest() -> None:
    """
    Executes the ingestion process.
    
    Reads the source CSV file, parses the technical data, adds an HQ arrival 
    timestamp, and saves the entries into the local database.
    """
    # 1. Ensure the database and tables are initialized
    init_db()
    
    # Check if the source file exists using Pathlib (from config)
    if not SOURCE_CSV.exists():
        print(f"[!] Source file not found: {SOURCE_CSV}")
        print("[!] Please ensure the Agent's data is placed in the 'data/inbox' directory.")
        return

    print(f"[*] Starting ingestion sequence for: {SOURCE_CSV.name}")
    
    processed_rows: List[Tuple] = []
    ingest_timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(SOURCE_CSV, mode='r', encoding='utf-8') as f:
            # DictReader handles the quoted SSIDs automatically
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                try:
                    # Construct data tuple with HQ metadata
                    data_entry = (
                        ingest_timestamp,
                        int(row['ID_LOCALITY']),
                        row['SSID'],
                        row['MAC / BSSID'],
                        int(row['RSSI']),
                        int(row['CHANNEL']),
                        int(row['HIDDEN']),
                        int(row['SECURITY'])
                    )
                    processed_rows.append(data_entry)
                except (KeyError, ValueError, TypeError) as e:
                    # Skip corrupted rows or header mismatches
                    continue
                    
    except Exception as e:
        print(f"[ERROR] Failed to read source file: {e}")
        return

    if processed_rows:
        # Batch save to database via the DB manager
        imported_count: Optional[int] = save_to_db(processed_rows)
        
        if imported_count:
            print(f"[OK] Successfully ingested {imported_count} records into the vault.")
            
            # Recommendation: Implement file archiving here to prevent duplicate imports
            # e.g., archive_source_file(SOURCE_CSV)
        else:
            print("[!] Database operation failed. No records were saved.")
    else:
        print("[!] Ingestion aborted: No valid data records found in source file.")


if __name__ == "__main__":
    run_ingest()