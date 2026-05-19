#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

# Add /app to sys.path to allow importing from app package
sys.path.insert(0, '/app')
from app.totp_utils import generate_totp_code

SEED_FILE_PATH = "/data/seed.txt"

def main():
    if not os.path.exists(SEED_FILE_PATH):
        print(f"Error: Seed file {SEED_FILE_PATH} not found", file=sys.stderr)
        return
        
    try:
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
            
        code = generate_totp_code(hex_seed)
        
        # Get current UTC timestamp
        now_utc = datetime.now(timezone.utc)
        timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{timestamp_str} - 2FA Code: {code}")
        
    except Exception as e:
        print(f"Error generating 2FA code: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
