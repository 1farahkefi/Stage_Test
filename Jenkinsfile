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

        stage('Run Flask App (background)') {
            steps {
                bat """
                    REM Démarrer Flask en tâche de fond avec redirection des logs
                    start /min cmd /c "%VENV%\\Scripts\\python.exe -m flask run --host=%FLASK_HOST% --port=%FLASK_PORT% > flask_output.log 2>&1"
                """
                // Attendre un peu pour que le serveur ait le temps de démarrer
                bat 'ping 127.0.0.1 -n 5 > nul'

                script {
                    def serverStarted = false
                    for (int i = 0; i < 30; i++) {
                        def response = bat(script: """
                            powershell -Command "try { (Invoke-WebRequest -Uri http://localhost:%FLASK_PORT% -UseBasicParsing).StatusCode } catch { Write-Output 'Error' }"
                        """, returnStdout: true).trim()
                        if (response == "200") {
                            serverStarted = true
                            break
                        }
                        sleep 1
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
                    %VENV%\\Scripts\\python.exe -m behave tests/Ederson
                    %VENV%\\Scripts\\python.exe -m behave tests/Livebox7
                """
            }
        }

        stage('Stop Flask Server') {
            steps {
                bat 'taskkill /IM python.exe /F || echo "Aucun processus python à tuer."'
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
