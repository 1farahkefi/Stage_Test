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

        stage('Creer un environnement virtuel') {
            steps {
                bat 'python -m venv .venv'
            }
        }

        stage('Installer les dependances') {
            steps {
                bat '.venv\\Scripts\\pip.exe install -r requirements.txt'
            }
        }

        stage('Build image Docker Flask') {
            steps {
                bat 'docker build -t flask_app_image .'
            }
        }

        stage('Lancer Flask ') {
            steps {
                bat 'start /MIN "" .venv\\Scripts\\python.exe app.py'
                bat 'powershell -Command "Start-Sleep -Seconds 5"'
            }
        }

        stage('Verifier si Flask repond') {
            steps {
                bat '''
                    @echo off
                    setlocal enabledelayedexpansion
                    set success=0
                    for /L %%i in (1,1,10) do (
                        powershell -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:5000 -UseBasicParsing).StatusCode } catch { 'Error' }" > response.txt
                        findstr /C:"200" response.txt > nul
                        if !errorlevel! == 1 (
                            powershell -Command "Start-Sleep -Seconds 1"
                        ) else (
                            set success=1
                            goto done
                        )
                    )
                    :done
                    if !success!==0 (
                        echo [ERREUR] Flask ne répond pas à temps.
                        type response.txt
                        exit /b 1
                    )
                '''
            }
        }

        stage('Lancer Selenium et Flask dans Docker') {
            steps {
                bat '''
                    docker network create test_network || exit 0

                    docker rm -f selenium || exit 0
                    docker rm -f flask_app || exit 0

                    docker run -d --name selenium --network test_network selenium/standalone-chrome
                    docker run -d --name flask_app --network test_network -p 5000:5000 flask_app_image
                '''
            }
        }

        stage('Executer le test Behave') {
            steps {
                bat "${PYTHON} -m behave tests/Livebox7/features"
            }
        }

        stage('Arreter Flask ') {
            steps {
                bat '''
                    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr LISTENING') do taskkill /PID %%a /F
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline termine'
        }
        failure {
            echo 'Echec du pipeline'
        }
    }
}