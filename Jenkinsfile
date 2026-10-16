pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ai-ecommerce-devops'
        IMAGE_TAG = '1.0'
        CONTAINER_NAME = 'ai-ecommerce-jenkins'
        APP_PORT = '8083'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Application') {
            steps {
                sh '''
                    set -eu
                    test -f application/index.html
                    test -f docker/Dockerfile
                    echo "Application files validated."
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu
                    docker build -f docker/Dockerfile \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    set -eu
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 0 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    set -eu
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      --restart unless-stopped \
                      -p ${APP_PORT}:80 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Verification') {
            steps {
                sh '''
                    set -eu
                    for attempt in $(seq 1 15); do
                        if curl -fsS http://127.0.0.1:${APP_PORT}/ \
                            -o /dev/null; then
                            echo "Health check passed."
                            exit 0
                        fi
                        sleep 2
                    done
                    echo "Health check failed."
                    docker logs ${CONTAINER_NAME}
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
