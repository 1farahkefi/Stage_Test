pipeline {
    agent any

    environment {
        VENV = ".venv"
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
        FLASK_HOST = "127.0.0.1"
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
                        exit 1
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
                        // Lancer Flask avec redirection du PID vers fichier en ASCII
                        bat """
                            chcp 65001
                            powershell -Command "$env:FLASK_APP='${env.FLASK_APP}'; $env:FLASK_ENV='${env.FLASK_ENV}'; $env:FLASK_RUN_PORT='${env.FLASK_PORT}'; $env:FLASK_RUN_HOST='${env.FLASK_HOST}'; Start-Process '${env.VENV}\\\\Scripts\\\\flask.exe' -NoNewWindow -RedirectStandardOutput 'flask_output.log' -PassThru | ForEach-Object { $_.Id } > flask.pid"
                        """

                        // Lire le PID proprement
                        flaskPID = readFile('flask.pid').trim()
                        echo "Flask PID = ${flaskPID}"

                        // Attendre que le serveur Flask réponde
                        timeout(time: 60, unit: 'SECONDS') {
                            waitUntil {
                                def response = bat(
                                    script: """powershell -Command "try { (Invoke-WebRequest -Uri http://localhost:${env.FLASK_PORT} -UseBasicParsing).StatusCode } catch { 'Error' }" """,
                                    returnStdout: true
                                ).trim()
                                echo "HTTP response: ${response}"
                                return response == "200"
                            }
                        }

                        echo "Serveur Flask démarré avec succès."

                        // Exécuter les tests Behave
                        bat """
                            ${env.VENV}\\Scripts\\python.exe -m behave bdd_tests/features/Ederson.feature > ederson.log
                            ${env.VENV}\\Scripts\\python.exe -m behave bdd_tests/features/Livebox7.feature > livebox7.log
                            type ederson.log
                            type livebox7.log
                        """

                    } finally {
                        if (flaskPID?.isInteger()) {
                            echo "Arrêt du serveur Flask (PID=${flaskPID})"
                            bat "taskkill /F /PID ${flaskPID}"
                        } else {
                            echo "PID Flask invalide ou introuvable : ${flaskPID}"
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
