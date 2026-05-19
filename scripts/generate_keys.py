from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_rsa_keypair(key_size: int = 4096):
    """Generate RSA 4096-bit key pair"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def main():
    print("Generating 4096-bit RSA key pair...")
    private_key, public_key = generate_rsa_keypair()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL, # PKCS#1
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save keys to parent directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    private_path = os.path.join(parent_dir, "student_private.pem")
    public_path = os.path.join(parent_dir, "student_public.pem")
    
    with open(private_path, "wb") as f:
        f.write(private_pem)
        
    with open(public_path, "wb") as f:
        f.write(public_pem)
        
    print(f"Keys generated successfully:\n- {private_path}\n- {public_path}")
    print("⚠️  SECURITY WARNING: These keys are for this assignment ONLY. Do NOT use them for real security purposes.")

if __name__ == "__main__":
    main()
