Write-Host "Starting local build process..."

# Make sure Minikube is running
Write-Host "Checking Minikube status..."
minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..."
    minikube start
}

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Run the tests
Write-Host "Running tests..."
pytest tests/

# Build the Docker image
Write-Host "Building Docker image..."
docker build -t user-service:latest .

# Load the image into Minikube
Write-Host "Loading image into Minikube..."
minikube image load user-service:latest

# Apply Kubernetes configuration
Write-Host "Deploying to Kubernetes..."
kubectl apply -f k8s/deployment.yaml

# Wait for deployment to complete
Write-Host "Waiting for deployment to complete..."
kubectl rollout status deployment/user-service

# Show status
Write-Host "Deployment status:"
kubectl get pods
kubectl get svc user-service

Write-Host "Build and deployment complete!"
Write-Host "To access the app, run: kubectl port-forward svc/user-service 8000:80"
