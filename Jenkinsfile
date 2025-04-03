pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "fastapi-app:${BUILD_NUMBER}"
        CONTAINER_NAME = "fastapi-container"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        
        stage('Test') {
            steps {
                echo "Running tests..."
                // Add your test commands here
                // Example: sh "docker run --rm ${DOCKER_IMAGE} pytest"
            }
        }
        
        stage('Deploy to Development Namespace') {
            steps {
                sh '''
                    # Create development namespace if it doesn't exist
                    kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
                    
                    # Load image to Minikube
                    minikube image load ${DOCKER_IMAGE}
                    
                    # Update the deployment file with the new image
                    sed -i "s|image: fastapi-app:latest|image: ${DOCKER_IMAGE}|g" deployment.yaml
                    
                    # Apply configurations to dev namespace
                    kubectl apply -f deployment.yaml -n dev
                    kubectl apply -f service.yaml -n dev
                    kubectl apply -f hpa.yaml -n dev
                    
                    # Wait for deployment to be ready
                    kubectl rollout status deployment/fastapi-app -n dev
                '''
            }
        }
        
        stage('Deploy to Production Namespace') {
            steps {
                input message: 'Deploy to production?', ok: 'Yes'
                
                sh '''
                    # Create production namespace if it doesn't exist
                    kubectl create namespace prod --dry-run=client -o yaml | kubectl apply -f -
                    
                    # Apply configurations to prod namespace
                    kubectl apply -f deployment.yaml -n prod
                    kubectl apply -f service.yaml -n prod
                    kubectl apply -f hpa.yaml -n prod
                    
                    # Scale for production workload
                    kubectl scale deployment fastapi-app --replicas=5 -n prod
                    
                    # Wait for deployment to be ready
                    kubectl rollout status deployment/fastapi-app -n prod
                '''
            }
        }
        
        stage('Get Service URLs') {
            steps {
                sh '''
                    echo "Development Service URL:"
                    minikube service fastapi-service -n dev --url
                    
                    echo "Production Service URL:"
                    minikube service fastapi-service -n prod --url
                '''
            }
        }
    }
    
    post {
        success {
            echo "Deployment completed successfully!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
