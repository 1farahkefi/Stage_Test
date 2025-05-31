pipeline {
    agent any

    environment {
        VENV = '.venv'
        FLASK_APP = 'app.py'  // Nom de ton fichier Flask
        FLASK_ENV = 'development'
    }

    stages {
        stage('Setup environment') {
            steps {
                script {
                    // Assure-toi que le virtualenv est activé (adapté selon ton environnement)
                    sh """
                        if [ -d $VENV ]; then
                            source $VENV/bin/activate
                        else
                            echo "Virtualenv $VENV non trouvé, créer et installer les dépendances..."
                            python3 -m venv $VENV
                            source $VENV/bin/activate
                            pip install -r requirements.txt
                        fi
                    """
                }
            }
        }

        stage('Start Flask app') {
            steps {
                script {
                    // Démarrer Flask en arrière-plan, rediriger la sortie, stocker le PID
                    sh """
                        source $VENV/bin/activate
                        nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                        echo \$! > flask.pid
                    """

                    // Attendre que Flask soit prêt (tu peux améliorer avec un check http)
                    sleep 10
                }
            }
        }

        stage('Run tests with Behave') {
            steps {
                script {
                    // Lancer behave dans le virtualenv
                    sh """
                        source $VENV/bin/activate
                        behave --no-capture -D env=jenkins
                    """

                    // OU si tu préfères appeler l’API Flask
                    // sh 'curl -X POST -u USER:PASSWORD http://localhost:5000/launch/livebox7'
                    // sh 'curl -X POST -u USER:PASSWORD http://localhost:5000/launch/ederson'
                }
            }
        }
    }

    post {
        always {
            script {
                // Arrêter Flask proprement si le PID existe
                def pid = sh(script: 'cat flask.pid || echo ""', returnStdout: true).trim()
                if (pid) {
                    echo "Arrêt du serveur Flask (PID $pid)..."
                    sh "kill $pid || true"
                } else {
                    echo "Pas de PID Flask trouvé, rien à arrêter."
                }
            }
        }
    }
}
