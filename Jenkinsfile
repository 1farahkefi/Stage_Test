pipeline {
    agent any

    environment {
        VENV = ".venv"
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
        FLASK_HOST = "0.0.0.0"
        FLASK_PORT = "5000"
    }
    stage('Clean Workspace') {
    steps {
        cleanWs()
    }
}

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/1farahkefi/Stage_Test.git'
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
        stage('Check requirements.txt') {
             steps {
                bat """
                    if not exist requirements.txt (
                    echo "requirements.txt introuvable !" && exit 1
                )
                """
             }
        }

        stage('Run Flask App (background)') {
            steps {
                script {
                    // Démarrer Flask en tâche de fond, rediriger la sortie dans un fichier log
                    bat """
                        start /min cmd /c "set FLASK_APP=%FLASK_APP% && set FLASK_ENV=%FLASK_ENV% && %VENV%\\Scripts\\python.exe -m flask run --host=%FLASK_HOST% --port=%FLASK_PORT% > flask_output.log 2>&1"
                    """

                    // Attendre un peu que le serveur démarre
                    sleep time: 5, unit: 'SECONDS'

                    // Vérifier que le serveur est accessible
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
                    %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Ederson.feature
                    %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Livebox7.feature
                """
            }
        }


        stage('Stop Flask Server') {
            steps {
                script {
                    // Tuer le processus Flask lancé sur le port 5000 (ou le port défini)
                    bat """
                        for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%FLASK_PORT% ^| findstr LISTENING') do taskkill /PID %%a /F
                    """
                }
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
