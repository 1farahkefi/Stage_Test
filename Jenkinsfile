pipeline {
    agent any

    environment {
        VENV = ".venv"
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
        FLASK_HOST = "0.0.0.0"
        FLASK_PORT = "5000"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/1farahkefi/Stage_Test.git'
            }
        }

        stage('Check requirements.txt') {
            steps {
                bat """
                    if not exist requirements.txt (
                        echo requirements.txt introuvable !
                        exit 1
                    )
                """
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat """
                    python -m venv %VENV%
                    %VENV%\\Scripts\\python.exe -m pip install --upgrade pip
                    %VENV%\\Scripts\\python.exe -m pip install -r requirements.txt
                """
            }
        }

        stage('Run Flask App (background)') {
            steps {
                script {
                    bat """
                        start /min cmd /c "set FLASK_APP=%FLASK_APP% && set FLASK_ENV=%FLASK_ENV% && %VENV%\\Scripts\\python.exe -m flask run --host=%FLASK_HOST% --port=%FLASK_PORT% > flask_output.log 2>&1"
                    """

                    sleep time: 5, unit: 'SECONDS'

                    def serverStarted = false
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def response = bat(
                                script: """powershell -Command "try { (Invoke-WebRequest -Uri http://localhost:%FLASK_PORT% -UseBasicParsing).StatusCode } catch { Write-Output 'Error' }" """,
                                returnStdout: true
                            ).trim()
                            if (response == "200") {
                                serverStarted = true
                                return true
                            }
                            sleep 2
                            return false
                        }
                    }
                    if (!serverStarted) {
                        error("Le serveur Flask n'a pas démarré dans le temps imparti.")
                    }
                }
            }
        }

        stage('Run Behave Tests') {
            steps {
                bat """
                    %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Ederson.feature > ederson.log
                    %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Livebox7.feature > livebox7.log
                    type ederson.log
                    type livebox7.log
                """
            }
        }

        stage('Stop Flask Server') {
            steps {
                bat """
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%FLASK_PORT% ^| findstr LISTENING') do taskkill /PID %%a /F
                """
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
            archiveArtifacts artifacts: '*.log, flask_output.log', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline exécuté avec succès !'
        }
        failure {
            echo 'Le pipeline a échoué.'
        }
    }
}
