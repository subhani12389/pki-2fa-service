import pyotp
import base64
import time

def hex_to_base32_seed(hex_seed: str) -> str:
    """Convert 64-character hex seed to base32 string"""
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode('utf-8')

def generate_totp_code(hex_seed: str) -> str:
    """Generate current TOTP code from hex seed"""
    base32_seed = hex_to_base32_seed(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """Verify TOTP code with time window tolerance"""
    base32_seed = hex_to_base32_seed(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)

def get_remaining_seconds() -> int:
    """Calculate remaining seconds in current 30s period"""
    return 30 - (int(time.time()) % 30)
