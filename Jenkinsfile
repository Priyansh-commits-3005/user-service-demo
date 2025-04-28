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
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
