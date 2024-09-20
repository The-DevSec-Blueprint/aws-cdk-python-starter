pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION    = 'us-east-1'  // Replace with your preferred region

        NEXUS_DOCKER_REGISTRY = '10.0.0.22:8082'
        SONAR_TOKEN = credentials('sonar-analysis')
        SNYK_TOKEN = credentials('snyk-api-token')
        SONAR_PROJECT_KEY = "aws-cdk-python-starter"
        SNYK_ORG_NAME = 'dsb-6YmccYk2Hr2e2suHMxA4KG'
    }

    stages {
        stage('Clone') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Gitea PAT', url: 'http://10.0.0.22/damien/aws-cdk-python-starter.git']])
            }
        }

        stage('Build & Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('CDK Synth') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cdk synth
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --cov=. --cov-report=xml:coverage.xml --junitxml=test-results/test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results/test-results.xml'
                }
            }
        }


        stage('Security Scan'){
            parallel {
                stage('Sonar Scan') {
                    steps {
                        script {
                            try{
                                withSonarQubeEnv(installationName: 'Sonar Server', credentialsId: 'sonar-analysis') {
                                    sh '''
                                    docker run --rm \
                                    -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
                                    -e SONAR_TOKEN="${SONAR_TOKEN}" \
                                    -v "$(pwd):/usr/src" \
                                    ${NEXUS_DOCKER_REGISTRY}/sonarsource/sonar-scanner-cli \
                                    -Dsonar.projectKey="${SONAR_PROJECT_KEY}" \
                                    -Dsonar.qualitygate.wait=true \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                                    -Dsonar.sources=.
                                    '''
                                }
                            } catch (Exception e) {
                                // Handle the error
                                echo "Quality Qate check has failed: ${e}"
                                currentBuild.result = 'UNSTABLE' // Mark the build as unstable instead of failing
                            }
                        }
                    }
                }
                stage('Synk Scan'){
                    steps{
                        sh '''
                        . .venv/bin/activate
                        snyk iac test --severity-threshold=high --org=${SNYK_ORG_NAME} --report
                        '''
                    }
                }
                stage('Trivy Scan') {
                    steps {
                        sh '''
                            trivy config --exit-code 0 --severity HIGH,CRITICAL cdk.out > trivy-report.txt
                        '''
                    }
                }
            }
        }

        stage('CDK Deploy') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cdk deploy --require-approval never
                '''
            }
        }

        stage('CDK Destroy') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cdk destroy --all --force
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
            cleanWs()
        }
    }
}
