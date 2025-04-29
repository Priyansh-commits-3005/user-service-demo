pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests/'
            }
        }
        stage('Start Minikube') {
            steps {
                bat 'minikube delete || echo "No existing minikube cluster"'
                bat 'minikube start --memory=3000 --cpus=2 --extra-config=kubelet.selinux-permissive=true'
                bat 'minikube status'
                bat 'timeout /t 30'  // Give API server time to stabilize
            }
        }        
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t user-service:latest .'
            }
        }
        
        stage('Push to Minikube') {
            steps {
                bat 'minikube image load user-service:latest'
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl --context=minikube apply -f k8s/deployment.yaml'
                bat 'kubectl --context=minikube rollout status deployment/user-service'
            }
        }
        stage('Verify Deployment') {
            steps {
                bat 'kubectl --context=minikube get pods'
                bat 'kubectl --context=minikube get svc user-service'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}