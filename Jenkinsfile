pipeline {
    agent any

    environment {
        VENV = '.venv'
        FLASK_APP = 'app.py'  // ou le nom de ton fichier Flask
        FLASK_ENV = 'development'
    }

    stages {
        stage('Start Flask app') {
            steps {
                script {
                    // Démarrer Flask en arrière-plan
                    // Attention : adapte la commande en fonction de ta config
                    sh 'nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 & echo $! > flask.pid'
                    // Attendre que Flask soit prêt
                    sleep 10
                }
            }
        }

        stage('Run tests with Behave') {
            steps {
                script {
                    // Option 1: lancer behave directement dans Jenkins (si les tests sont locaux)
                    sh 'behave --no-capture -D env=jenkins'

                    // Option 2: ou appeler les endpoints Flask qui lancent behave (si tu veux tester l’intégration)
                    // Remplace USER et PASSWORD par des credentials valides
                    // sh 'curl -X POST -u USER:PASSWORD http://localhost:5000/launch/livebox7'
                    // sh 'curl -X POST -u USER:PASSWORD http://localhost:5000/launch/ederson'
                }
            }
        }
    }

    post {
        always {
            script {
                // Arrêter Flask proprement
                def pid = sh(script: 'cat flask.pid', returnStdout: true).trim()
                if (pid) {
                    sh "kill $pid || true"
                }
            }
        }
    }
}
