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

        stage('Préparation de l’environnement') {
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
/*
        stage('Build Docker image for Flask app') {
            steps {
                bat 'docker build -t flask_app_image .'
            }
        }

        stage('Start Selenium and Flask containers') {
            steps {
                bat '''
                    docker network create test_network || true

                    docker rm -f selenium || true
                    docker rm -f flask_app || true

                    docker run -d --name selenium --network test_network selenium/standalone-chrome
                    docker run -d --name flask_app --network test_network -p 5000:5000 flask_app_image
                '''
            }
        }
*/
stage('SonarQube analysis') {
            steps {
                // Utilise la config SonarQube installée et le token associé
                withSonarQubeEnv('sonar_token') {
                    // Exécute le scanner depuis l'outil installé automatiquement
                    sh 'sonar-scanner -Dsonar.projectKey=1farahkefi_Stage_Test -Dsonar.sources=.'
                }
            }
        }


        stage("Vérifier la qualité (SonarQube)") {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Lancer tests Behave Ederson') {
            steps {
                bat '.venv\\Scripts\\python.exe -m behave tests/Ederson/features'
            }
        }

        stage('Lancer tests Behave livebox7') {
            steps {
                bat '.venv\\Scripts\\python.exe -m behave tests/Livebox7/features'
            }
        }

        stage('Arrêter Flask') {
            steps {
                bat '''
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
