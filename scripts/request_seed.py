import requests
import json
import os

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_key_path = os.path.join(parent_dir, "student_public.pem")
    
    if not os.path.exists(public_key_path):
        print("Error: student_public.pem not found. Run generate_keys.py first.")
        return
        
    with open(public_key_path, "r") as f:
        public_key_pem = f.read()
        
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }
    
    print(f"Requesting seed for {student_id} at {github_repo_url}...")
    
    try:
        response = requests.post(
            API_URL, 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            encrypted_seed = data.get("encrypted_seed")
            seed_path = os.path.join(parent_dir, "encrypted_seed.txt")
            with open(seed_path, "w") as f:
                f.write(encrypted_seed)
            print(f"Success! Encrypted seed saved to {seed_path}")
        else:
            print(f"API returned error: {data}")
            
    except Exception as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response details: {e.response.text}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Request encrypted seed from instructor API")
    parser.add_argument("--student-id", required=True, help="Your Student ID")
    parser.add_argument("--repo-url", required=True, help="Your exact GitHub repository URL")
    
    args = parser.parse_args()
    request_seed(args.student_id, args.repo_url)
