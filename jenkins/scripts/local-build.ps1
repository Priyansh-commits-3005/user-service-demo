Write-Host "Starting local build process..."

# Install dependencies
pip install -r requirements.txt

# Run the tests
pytest tests/

# Build the Docker image
docker build -t user-service:latest .

# Load the image into Minikube
minikube image load user-service:latest

# Apply Kubernetes configuration
kubectl apply -f k8s/deployment.yaml

Write-Host "Build and deployment complete!"
