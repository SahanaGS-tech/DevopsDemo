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
            script {
                // Use shell to get IP and build Docker image
                sh '''
                    # Get host IP
                    HOST_IP=$(hostname -I | awk '{print $1}')
                    
                    # SSH and build Docker image
                    ssh vboxuser@$HOST_IP "cd ${WORKSPACE} && docker build -t ${DOCKER_IMAGE} ."
                '''
            }
        }
    }
    
    stage('Deploy to Kubernetes') {
        steps {
            script {
                // Use shell to get IP and deploy to Kubernetes
                sh '''
                    # Get host IP
                    HOST_IP=$(hostname -I | awk '{print $1}')
                    
                    # SSH and deploy to Kubernetes
                    ssh vboxuser@$HOST_IP "cd ${WORKSPACE} && \
                    minikube image load ${DOCKER_IMAGE} && \
                    kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f - && \
                    sed -i "s|image: fastapi-app:latest|image: ${DOCKER_IMAGE}|g" deployment.yaml && \
                    kubectl apply -f deployment.yaml -n dev && \
                    kubectl apply -f service.yaml -n dev && \
                    kubectl apply -f hpa.yaml -n dev && \
                    kubectl rollout status deployment/fastapi-app -n dev"
                '''
            }
        }
    }
}