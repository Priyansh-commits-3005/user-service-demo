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
                bat 'minikube status || minikube start'
                bat 'minikube status'
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
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl rollout status deployment/user-service'

            }
        }
        stage('Verify Deployment') {
            steps {
                bat 'kubectl get pods'
                bat 'kubectl get svc user-service'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
