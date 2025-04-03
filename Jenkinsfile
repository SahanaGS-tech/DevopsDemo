pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "fastapi-app:${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    # Run this on the host where Docker is working
                    ssh vboxuser@hostname -I | awk '{print $1}' "cd ${WORKSPACE} && docker build -t ${DOCKER_IMAGE} ."
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    # Run these commands on the host
                    ssh vboxuser@hostname -I | awk '{print $1}' "cd ${WORKSPACE} && \
                    minikube image load ${DOCKER_IMAGE} && \
                    kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f - && \
                    sed -i 's|image: fastapi-app:latest|image: ${DOCKER_IMAGE}|g' deployment.yaml && \
                    kubectl apply -f deployment.yaml -n dev && \
                    kubectl apply -f service.yaml -n dev && \
                    kubectl apply -f hpa.yaml -n dev && \
                    kubectl rollout status deployment/fastapi-app -n dev"
                '''
            }
        }
    }
}
