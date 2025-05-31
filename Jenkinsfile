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

        stage('Preparation') {
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

        stage('Tester si Flask répond') {
            steps {
                bat '''
                    @echo off
                    setlocal enabledelayedexpansion
                    set success=0
                    for /L %%i in (1,1,10) do (
                        powershell -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:5000 -UseBasicParsing).StatusCode } catch { 'Error' }" > response.txt
                        findstr /C:"200" response.txt > nul
                        if !errorlevel! == 0 (
                            set success=1
                            goto done
                        )
                        powershell -Command "Start-Sleep -Seconds 1"
                    )
                    :done
                    if %success%==0 (
                        echo Flask n'a pas répondu à temps.
                        type response.txt
                        exit /b 1
                    )
                    exit /b 0
                '''
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