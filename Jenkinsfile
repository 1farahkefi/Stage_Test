pipeline {
    agent any

    environment {
        VENV = ".venv"
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/1farahkefi/Stage_Test.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App (background)') {
            steps {
                sh '''
                source $VENV/bin/activate
                nohup flask run --host=0.0.0.0 > flask_output.log 2>&1 &
                sleep 5
                '''
            }
        }

        stage('Run Behave Tests') {
            steps {
                sh '''
                source $VENV/bin/activate
                behave tests/Ederson || true
                behave tests/Livebox7 || true
                '''
            }
        }

        stage('Stop Flask Server') {
            steps {
                sh '''
                pkill -f "flask run"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
            archiveArtifacts artifacts: 'flask_output.log', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline exécuté avec succès !'
        }
        failure {
            echo 'Le pipeline a échoué.'
        }
    }
}
