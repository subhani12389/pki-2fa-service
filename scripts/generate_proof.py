import subprocess
import os
import base64
import sys

# Add parent dir to sys.path to allow importing from app package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.crypto_utils import sign_message, encrypt_with_public_key, load_private_key, load_public_key

def main():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Get current commit hash
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%H'],
            cwd=parent_dir,
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
        if not commit_hash:
            raise Exception("Empty commit hash")
    except Exception as e:
        print("Error getting commit hash. Make sure you have committed your changes.", file=sys.stderr)
        return

    print(f"Commit Hash: {commit_hash}")
    
    # 2. Load student private key
    private_key_path = os.path.join(parent_dir, "student_private.pem")
    if not os.path.exists(private_key_path):
        print("Error: student_private.pem not found.", file=sys.stderr)
        return
    private_key = load_private_key(private_key_path)
    
    # 3. Sign commit hash with student private key
    # (sign_message handles utf-8 encoding of the string)
    signature_bytes = sign_message(commit_hash, private_key)
    
    # 4. Load instructor public key
    instructor_key_path = os.path.join(parent_dir, "instructor_public.pem")
    if not os.path.exists(instructor_key_path):
        print("Error: instructor_public.pem not found. Download it from the course resources.", file=sys.stderr)
        return
    instructor_public_key = load_public_key(instructor_key_path)
    
    # 5. Encrypt signature with instructor public key
    encrypted_signature = encrypt_with_public_key(signature_bytes, instructor_public_key)
    
    # 6. Base64 encode encrypted signature (single line)
    b64_encrypted_signature = base64.b64encode(encrypted_signature).decode('utf-8').replace('\n', '')
    
    print("\n--- Encrypted Commit Signature ---")
    print(b64_encrypted_signature)
    print("----------------------------------")

if __name__ == "__main__":
    main()
