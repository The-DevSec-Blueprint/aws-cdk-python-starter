pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION    = 'us-east-1'  // Replace with your preferred region
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

        stage('CDK Deploy') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cdk deploy --require-approval never
                '''
            }
        }
    }
}
