pipeline {
    agent any
    environment {
        IMAGE_REPOSITORY = 'mananshori98/aceest-fitness-devops'
        RELEASE_TAG = 'v2.0.0'
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Set Up Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Validate and Test') {
            steps {
                sh '.venv/bin/python -m py_compile app.py'
                sh '.venv/bin/python -m pytest -q --cov=app --cov-report=term --cov-report=xml'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Build and Test Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_REPOSITORY}:${RELEASE_TAG} .'
                sh 'docker run --rm ${IMAGE_REPOSITORY}:${RELEASE_TAG} python -m pytest -q'
                sh 'docker tag ${IMAGE_REPOSITORY}:${RELEASE_TAG} ${IMAGE_REPOSITORY}:latest'
            }
        }
        stage('Publish Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh 'echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push ${IMAGE_REPOSITORY}:${RELEASE_TAG}'
                    sh 'docker push ${IMAGE_REPOSITORY}:latest'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f kubernetes/base.yaml'
                sh 'kubectl -n aceest rollout status deployment/aceest-fitness --timeout=120s'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
            sh 'docker logout || true'
            cleanWs()
        }
        success { echo 'ACEest Assignment 2 pipeline completed successfully.' }
        failure { echo 'Pipeline failed. Review the failed stage.' }
    }
}
