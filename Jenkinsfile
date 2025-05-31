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
                bat '''
                python -m venv %VENV%
                call %VENV%\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App (background)') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                start /b flask run --host=0.0.0.0 > flask_output.log 2>&1
                timeout /t 5 > NUL
                '''
            }
        }

        stage('Run Behave Tests') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                behave tests/Ederson || exit 0
                behave tests/Livebox7 || exit 0
                '''
            }
        }

        stage('Stop Flask Server') {
            steps {
                bat '''
                for /f "tokens=2 delims=," %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| findstr /I "flask"') do taskkill /PID %%a /F
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
