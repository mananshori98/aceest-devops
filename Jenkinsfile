pipeline {
    // Same Python minor version as the Dockerfile and GitHub Actions workflow
    agent {
        docker { image 'python:3.12-slim' }
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --tb=short
                '''
            }
        }
    }
}
