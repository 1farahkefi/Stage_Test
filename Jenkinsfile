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
                bat '''
                    if not exist requirements.txt (
                        echo requirements.txt introuvable !
                        exit /b 1
                    )
                '''
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

        stage('Run Flask App and Behave Tests') {
            steps {
                script {
                    def flaskPID = null
                    try {
                        // Lancer Flask en tâche de fond avec PowerShell et récupérer le PID
                        bat """
                            powershell.exe -NoProfile -Command "Start-Process -FilePath '%VENV%\\\\Scripts\\\\python.exe' -ArgumentList '-m flask run --host=%FLASK_HOST% --port=%FLASK_PORT%' -PassThru | Select-Object -ExpandProperty Id > flask.pid"
                        """

                        // Lire le PID dans une variable Groovy
                        flaskPID = readFile('flask.pid').trim()
                        echo "Flask PID = ${flaskPID}"

                        // Attendre que Flask soit dispo (HTTP 200)
                        timeout(time: 60, unit: 'SECONDS') {
                            waitUntil {
                                def response = bat(
                                    script: """powershell.exe -NoProfile -Command "try { (Invoke-WebRequest -Uri http://localhost:%FLASK_PORT% -UseBasicParsing).StatusCode } catch { Write-Output 'Error' }" """,
                                    returnStdout: true
                                ).trim()
                                echo "HTTP response: ${response}"
                                return response == "200"
                            }
                        }

                        echo "Serveur Flask démarré avec succès."

                        // Lancer les tests behave
                        bat """
                            %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Ederson.feature > ederson.log
                            %VENV%\\Scripts\\python.exe -m behave bdd_tests/features/Livebox7.feature > livebox7.log
                            type ederson.log
                            type livebox7.log
                        """

                    } finally {
                        if (flaskPID) {
                            echo "Arrêt du serveur Flask (PID=${flaskPID})"
                            bat "taskkill /PID ${flaskPID} /F"
                        }
                    }
                }
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
