from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from .crypto_utils import decrypt_seed, load_private_key
from .totp_utils import generate_totp_code, verify_totp_code, get_remaining_seconds

app = FastAPI()

SEED_FILE_PATH = "/data/seed.txt"
PRIVATE_KEY_PATH = "/app/student_private.pem"

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def api_decrypt_seed(req: DecryptRequest):
    try:
        if not os.path.exists(PRIVATE_KEY_PATH):
            raise Exception("Private key not found")
        private_key = load_private_key(PRIVATE_KEY_PATH)
        decrypted = decrypt_seed(req.encrypted_seed, private_key)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(SEED_FILE_PATH), exist_ok=True)
        with open(SEED_FILE_PATH, "w") as f:
            f.write(decrypted)
            
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Decryption failed"})

@app.get("/generate-2fa")
def api_generate_2fa():
    if not os.path.exists(SEED_FILE_PATH):
        return JSONResponse(status_code=500, content={"error": "Seed not decrypted yet"})
        
    with open(SEED_FILE_PATH, "r") as f:
        hex_seed = f.read().strip()
        
    try:
        code = generate_totp_code(hex_seed)
        valid_for = get_remaining_seconds()
        return {"code": code, "valid_for": valid_for}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/verify-2fa")
def api_verify_2fa(req: VerifyRequest):
    if not req.code:
        return JSONResponse(status_code=400, content={"error": "Missing code"})
        
    if not os.path.exists(SEED_FILE_PATH):
        return JSONResponse(status_code=500, content={"error": "Seed not decrypted yet"})
        
    with open(SEED_FILE_PATH, "r") as f:
        hex_seed = f.read().strip()
        
    try:
        is_valid = verify_totp_code(hex_seed, req.code, valid_window=1)
        return {"valid": is_valid}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
