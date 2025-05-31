pipeline {
    agent any

    environment {
        VENV = '.venv'
        PYTHON = '.venv\\Scripts\\python.exe'
        PIP = '.venv\\Scripts\\pip.exe'
    }

    stages {
        stage('Préparation') {
            steps {
                bat 'python -m venv .venv'
            }
        }

        stage('Install requirements') {
            steps {
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Lancer Flask') {
            steps {
                bat '''
                    set FLASK_APP=app.py
                    set FLASK_ENV=development
                    start /B .venv\\Scripts\\python.exe -m flask run --host=127.0.0.1 --port=5000
                '''
                // attendre 5 secondes
                bat 'timeout /t 5 > nul'
            }
        }

        stage('Tester si Flask répond') {
            steps {
                bat '''
                    for /L %%i in (1,1,10) do (
                        powershell -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:5000 -UseBasicParsing).StatusCode } catch { 'Error' }" > response.txt
                        findstr /C:"200" response.txt && exit /b 0
                        timeout /t 1 > nul
                    )
                    echo Flask n'a pas répondu à temps.
                    type response.txt
                    exit /b 1
                '''
            }
        }

        stage('Lancer tests Behave') {
            steps {
                bat '.venv\\Scripts\\behave'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}
