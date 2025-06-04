pipeline {
    agent any

    environment {
        VENV = '.venv'
        PYTHON = '.venv\\Scripts\\python.exe'
        PIP = '.venv\\Scripts\\pip.exe'
        DATABASE_URL = 'postgresql+psycopg2://postgres.ckbimfasdfzgiduhonty:SagemCom01%@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Preparation de l environment') {
            steps {
                bat 'python -m venv .venv'
            }
        }

        stage('Install requirements') {
            steps {
                bat '.venv\\Scripts\\pip.exe install -r requirements.txt'
            }
        }



        stage('Lancer Flask') {
            steps {
                bat 'start /MIN "" .venv\\Scripts\\python.exe app.py'
                bat 'powershell -Command "Start-Sleep -Seconds 5"'
            }
        }

        stage('Build Docker image for Flask app') {
            steps {
                script {
                    // Construire l'image Flask app (à partir de ton Dockerfile)
                    bat 'docker build -t flask_app_image .'
                }
            }
        }

        stage('Start Selenium and Flask containers') {
            steps {
                script {
                    // Lancer Selenium (ex: selenium/standalone-chrome) et Flask app
                    bat '''
                    docker network create test_network || true

                     # Supprimer les conteneurs s'ils existent
                        docker rm -f selenium || true
                        docker rm -f flask_app || true

                     # Lancer les conteneurs
                        docker run -d --name selenium --network test_network selenium/standalone-chrome
                        docker run -d --name flask_app --network test_network -p 5000:5000 flask_app_image
            '''
                }
            }
        }

        stage('Analyse SonarQube') {
            steps {
                withSonarQubeEnv('MySonar') {
                    bat 'sonar-scanner'
                }
            }
        }


        stage('Lancer tests Behave Ederson ') {
            steps {
                bat '.venv\\Scripts\\python.exe -m behave tests/Ederson/features'

            }
        }
        stage('Lancer tests Behave livebox7 ') {
            steps {
                bat '.venv\\Scripts\\python.exe -m behave tests/Livebox7/features'

            }
        }


        stage('Arrêter Flask') {
            steps {
                bat '''
                    REM Kill Flask (python.exe) sur le port 5000
                    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr LISTENING') do taskkill /PID %%a /F
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}