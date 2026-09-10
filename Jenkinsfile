pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    echo "===== Environment ====="
                    java --version
                    python3 --version
                    git --version
                '''
            }
        }

        stage('Repository Check') {
            steps {
                sh '''
                    echo "===== Repository ====="
                    pwd
                    ls -la
                '''
            }
        }
    }
}
