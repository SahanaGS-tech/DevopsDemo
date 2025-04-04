node {
    def DOCKER_IMAGE = "fastapi-app:${BUILD_NUMBER}"
    
    stage('Checkout') {
        checkout scm
    }
    
    stage('Build Docker Image') {
        sh "docker build -t ${DOCKER_IMAGE} ."
        sh "echo 'Docker image built: ${DOCKER_IMAGE}'"
    }
    
    stage('Test') {
        sh "echo 'Running tests...'"
        // Uncomment if you have tests
        // sh "docker run --rm ${DOCKER_IMAGE} pytest"
    }
    
    stage('Deploy to Kubernetes') {
        sh """
            # Create development namespace if it doesn't exist
            kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
            
            # Load image to Minikube
            minikube image load ${DOCKER_IMAGE}
            
            # Update the deployment YAML with the new image
            sed -i 's|image: fastapi-app:latest|image: ${DOCKER_IMAGE}|g' deployment.yaml
            
            # Apply Kubernetes manifests
            kubectl apply -f deployment.yaml -n dev
            kubectl apply -f service.yaml -n dev
            kubectl apply -f hpa.yaml -n dev
            
            # Wait for deployment to complete
            kubectl rollout status deployment/fastapi-app -n dev
        """
    }
    
    stage('Verify Deployment') {
        sh """
            # Get service URL
            echo "Service URL:"
            minikube service fastapi-service -n dev --url
            
            # Check deployments and pods
            echo "\\nDeployments:"
            kubectl get deployments -n dev
            
            echo "\\nPods:"
            kubectl get pods -n dev
            
            echo "\\nServices:"
            kubectl get services -n dev
        """
    }
}
