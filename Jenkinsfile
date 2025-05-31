pipeline {
    agent any

    environment {
    VENV = '.venv'
    PYTHON = '.venv\\Scripts\\python.exe'
    PIP = '.venv\\Scripts\\pip.exe'
    DATABASE_URL = 'postgresql+psycopg2://postgres:ton_mot_de_passe@host:port/base'
    SECRET_KEY = 'une_clef_secrete_pour_flask'
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
        bat '''
            start /MIN "" .venv\\Scripts\\python.exe app.py
            timeout /t 5 > nul
        '''
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
                        timeout /t 1 > nul
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

        stage('Lancer tests Behave') {
            steps {
                bat '.venv\\Scripts\\python.exe -m behave'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}
