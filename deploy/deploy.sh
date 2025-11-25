REMOTE=$1
KEY=$2

if [[ -z "$REMOTE" || -z "$KEY" ]]; then
  echo "Usage: $0 user@ip key.pem"
  exit 1
fi

echo "--- 🚀 Starting Deployment to $REMOTE ---"

echo "Step 1: Creating directory..."
ssh -o StrictHostKeyChecking=no -i "$KEY" "$REMOTE" "mkdir -p ~/aws-toolkit"

echo "Step 2: Copying files..."
scp -i "$KEY" -r toolkit requirements.txt "$REMOTE:~/aws-toolkit/"

echo "Step 3: Installing dependencies..."
ssh -i "$KEY" "$REMOTE" "
    # Check if python3 is installed
    if ! command -v python3 &> /dev/null; then
        echo 'Python3 not found, installing...';
        sudo yum install python3 -y;
    fi
    
    # Create venv if it doesn't exist
    python3 -m venv ~/aws-toolkit/venv || true
    
    # Activate and install requirements
    source ~/aws-toolkit/venv/bin/activate
    pip install -r ~/aws-toolkit/requirements.txt || true
"

echo "--- ✅ Deployed Successfully to $REMOTE ---"