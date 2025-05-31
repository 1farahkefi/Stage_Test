pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Démarrer les services Docker Compose') {
            steps {
                sh 'docker-compose up -d'
                // Attendre quelques secondes que Flask démarre correctement
                sleep(time: 10, unit: 'SECONDS')
            }
        }

        stage('Tester si Flask répond') {
            steps {
                sh '''
                    status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)
                    if [ "$status" -ne 200 ]; then
                        echo "Erreur : Flask ne répond pas (status=$status)"
                        exit 1
                    fi
                '''
            }
        }

        stage('Lancer tests Behave') {
            steps {
                // Exécuter les tests Behave à l'intérieur du conteneur Flask
                sh 'docker exec flask_app python -m behave tests'
            }
        }

        stage('Arrêter les services') {
            steps {
                sh 'docker-compose down'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
    }
}
